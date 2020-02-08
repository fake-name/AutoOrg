import os.path
# To change this template, choose Tools | Templates
# and open the template in the editor.
import sys
import os
import re
import math
import Levenshtein as Lv
import timeit
import numpy as np
import tempfile

import wx

import h5py


def compStr(strA, strB):
	'''
	Compare two strings. Do some fancy things to allow word transposition
	in the strings, and handle one string being a substring of the other
	intelligently.
	'''
	sLAt = strA.split(" ")
	sLBt = strB.split(" ")

	lenSLAt = len(sLAt)
	lenSLBt = len(sLBt)

	if lenSLAt < lenSLBt:
		sLA    = sLAt
		sLB    = sLBt
		lenSLA = lenSLAt
		lenSLB = lenSLBt
	else:
		sLA    = sLBt
		sLB    = sLAt
		lenSLA = lenSLBt
		lenSLB = lenSLAt

	totalSim = 0

	# The magic (or obsfucation, take your pick)
	for x in range(lenSLA):
		if len(sLA[x]) > 1:
			wordSimilarity = 0
			wordWeight = 0
			for y in range(lenSLB):
					compRatio = Lv.ratio(sLA[x], sLB[y])
					if compRatio > wordSimilarity:
						wordSimilarity = compRatio
						lenX = len(sLA[x])
						lenY = len(sLB[y])
						wordWeight = float(lenX if lenX < lenY else lenY)
						wordWeight = wordWeight - abs(lenX - lenY)
			if wordWeight > 0:
				totalSim += wordSimilarity * math.sqrt(wordWeight)

	divRatio = lenSLA if lenSLA > lenSLB else lenSLB
	if divRatio == 0:
		# print(totalSim, divRatio)
		return 0
	return totalSim / divRatio


class Filename():

	gid = None

	def __init__(self, filename, config, id_num):

		print("Comparing:", filename)
		self.similarity_cache = None

		self.__id_no = id_num

		#print "PreClean", filename
		tempCleaned = filename
		if config.brackets:
			tempCleaned = re.sub(r"\[.*?\]", " ", tempCleaned)
		if config.parentheses:
			tempCleaned = re.sub(r"\(.*?\)", " ", tempCleaned)
		if config.curlyBraces:
			tempCleaned = re.sub(r"\{.*?\}", " ", tempCleaned)

		#print "PostClean", tempCleaned
		tempCleaned = re.sub("'", "", tempCleaned)
		#remove punctuation cleanly (')apostrophes

		tempCleaned = re.sub(r"\.rar|\.zip|\.cbr|\.cbz|\.7z|\.jpg|\.png", " ", tempCleaned, re.IGNORECASE)	#remove known file suffixes
		tempCleaned = re.sub(r"([\[\]_\+0-9()=!,])", " ", tempCleaned)				#clean brackets, symbols, and numbers: Removed "-"
		tempCleaned = re.sub(r"\W(ch|vol)[0-9]+?", " ", tempCleaned)				#Clean 'ch01' or similar
		tempCleaned = re.sub(r"\W[vc][0-9]*?\W", " ", tempCleaned)				#Clean 'v01' and 'c01' or similar
		tempCleaned = re.sub(r"\W[a-zA-z0-9]\W", " ", tempCleaned)				#Remove all single letters

		for term in [t for t in config.stripTerms if t]:
			tempRE = re.compile(term, re.IGNORECASE)
			tempCleaned = tempRE.sub(" ", tempCleaned)

		tempCleaned = re.sub(r"\.", " ", tempCleaned).lower()					#Remove dots
		tempCleaned = re.sub(r" +", " ", tempCleaned).rstrip().lstrip()				#reduce all repeated spaces to one space

		self.fn = filename
		self.cn = tempCleaned

	@property
	def id_num(self):
		return self.__id_no

	def __repr__(self):
		return "<Filename id: %s, '%s:%s'>" % (self.__id_no, self.fn, self.cn)

	def __lt__(self, other):
		return self.fn < other.fn

	def __eq__(self, other):
		return self.fn == other.fn

	def __hash__(self):
		return self.__id_no


	def comp(self, otherFile):
		compValue = compStr(self.cn, otherFile.cn)
		return compValue
		#compConf.mapMatrice[otherFile.id_num, self.id_num] = compValue


	def purge(self, sMatrix, thresh = 1.3):
		for key, value in list(self.pairs.items()):
			if value < thresh:
				del self.pairs[key]
				#print "removed key", value, thresh
				#print type(value), type(thresh)
				#print value, thresh, value < thresh
				#print "Deling Key", key.fn



	#def __repr__(self):
	#	return (repr((self.fn, self.cn, self.pairs)))

class ConfigObj(object):
	compThreshold           = 1500

	wordLengthWeighting     = 1000
	strLengthWeighting      = 1000
	wordDifferenceWeighting = 1000

	stripTerms              = []
	stripStr                = ""

	brackets                = True
	parentheses             = True
	curlyBraces             = True

	mappingDict             = {}
	target_dir              = "~/"

	def getCompThresh(self):
		return float(self.compThreshold)/1000

	def dump(self):
		config = {}
		config["target_dir"]               = self.target_dir
		config["compThreshold"]            = self.compThreshold

		config["wordLengthWeighting"]      = self.wordLengthWeighting
		config["strLengthWeighting"]       = self.strLengthWeighting
		config["wordDifferenceWeighting	"] = self.wordDifferenceWeighting

		config["stripTerms"]               = self.stripTerms
		config["stripStr"]                 = self.stripStr

		config["brackets"]                 = self.brackets
		config["parentheses"]              = self.parentheses
		config["curlyBraces"]              = self.curlyBraces

		return config

	def load(self, config):

		self.target_dir               = config["target_dir"]
		self.compThreshold            = config["compThreshold"]
		self.wordLengthWeighting      = config["wordLengthWeighting"]
		self.strLengthWeightingconfig = config["strLengthWeighting"]
		self.wordDifferenceWeighting  = config["wordDifferenceWeighting	"]

		self.stripTerms               = config["stripTerms"]
		self.stripStr                 = config["stripStr"]

		self.brackets                 = config["brackets"]
		self.parentheses              = config["parentheses"]
		self.curlyBraces              = config["curlyBraces"]

		return

class ComutativeMatrix(object):
	# Matrix of simlarity values
	# Setting array[fileid_num1, fileid_num2] = simVal adds item to array
	# reading is accomplished by x = array[fileid_num1, fileid_num2]
	# since the similarity between two items is commutative ( array[fileid_num1, fileid_num2] ==  array[fileid_num2, fileid_num1] ),
	# if we always sort the arguments passed through __getattr__ so the larger one is first, reduncancy should be eliminated
	# Therefore The order which you pass items, both to read and write is not important
	# It should store the minimum ammount of information to hold the entirety of all comparison items

	def __init__(self, matrixSz):
		self.matrixSz = matrixSz

		if matrixSz > 5000:
			print()
			self.mmapped = True
			self.tempF = tempfile.mkstemp()
			self.f = h5py.File(self.tempF[1], 'w')

			self.m = self.f.create_dataset('ds', (matrixSz,matrixSz), compression='gzip', compression_opts=4)

			print("Initializing Array Tempfile - \"%s\"" % self.tempF[1])
			if matrixSz > 5000:
				print("This could take a while")
			#self.m[:] = -1		#Broadcast array to -1
			print("Array Initialized")
			#print self.m[:]
			#print self.m.items()
		else:
			print("Using in-memory array")
			self.mmapped = False
			self.m = np.zeros((matrixSz,matrixSz))

	def get(self, x, y):
		if x <= y:
			return self.m[x, y]
		else:
			return self.m[y, x]

	def __getitem__(self, key):
		if key[0] <= key[1]:
			return self.m[key[0], key[1]]
		else:
			return self.m[key[1], key[0]]

	def __setitem__(self, key, value):
		if key[0] <= key[1]:
			self.m[key[0], key[1]] = value
		else:
			self.m[key[1], key[0]] = value

	def set_row(self, index, rowDat):
		self.m[index,...] = rowDat

	def retItems(self, key, thresh):
		#print thresh
		out = {}
		xRang = self.m[...,key]
		yRang = self.m[key,...]
		for idx in range(self.matrixSz):
			sim = xRang[idx] if xRang[idx] > yRang[key] else yRang[key]
			if sim > thresh and idx != key:
				out[idx] = sim
		return out

	def __del__(self):
		if self.mmapped:
			try:
				self.f.close()
			except Exception:
				print("Could not close database file due to an unknown reason")

			try:
				os.close(self.tempF[0])
			except Exception:
				print("Could not close pipe")

			try:
				os.unlink(self.tempF[1])
			except Exception:
				print("Could not delete temporary database file at - %s" % self.tempF[1], "due to an unknown error")
				print("You may want to delete it manually")

	def close(self):
		self.__del__()


class Comparator():
	def __init__(self, compConf = ConfigObj):

		self.file_set = set()
		self.mapMatrice = None

		self.compConf = compConf

	def load_files(self, target_dir):
		# print("Getting File List...")

		dirCont = []
		if not os.access(target_dir, os.W_OK):
			print("cannot access Directory")
			return 0

		dirCont = os.listdir(target_dir)

		if not dirCont:
			print("No files in target Directory!")
			return 0

		#Import list of file names, and push them into a dictionary
		# print("Number of Files = %s" % len(dirCont))
		# print("Scrubbing File Names of Dirs")
		file_id = 0
		self.file_set = set()
		for item in dirCont:
			if os.path.isfile(os.path.join(target_dir, item)):
				file = Filename(
						filename = item,
						config   = self.compConf,
						id_num   = file_id,
					)
				self.file_set.add(file)
				if file_id % 250 == 0:
					print("File %s of %s" % (file_id, len(dirCont)))
				file_id += 1

		return len(self.file_set)

	def comp(self, targetDir):

		num_files = self.load_files(targetDir)
		if not num_files:
			return

		self.mapMatrice = ComutativeMatrix(num_files)
		for idx, targetFile in enumerate(self.file_set):

			for compFile in self.file_set:
				if (
						targetFile != compFile
					and
						targetFile.id_num >= compFile.id_num
					):
					self.mapMatrice[compFile.id_num, targetFile.id_num] = targetFile.comp(compFile)

			#Print **more** for lots of files, because each step takes longer
			#This makes progress more visible
			if num_files < 1000:
				modu = 25
			elif num_files < 5000:
				modu = 10
			else:
				modu = 1

			if idx % modu == 0:
				print("Step:", idx, end=' ')
				print(" - Remaning steps:", num_files - idx)

		#print self.mapMatrice

		#mx = self.mapMatrice.m
		#print mx[:]

	def trimTree(self, compThresh = 1.5):

		compThresh = float(compThresh)

		item_id_dict = {}

		for value in self.file_set:
			item_id_dict[value.id_num] = value

		# import pdb
		# pdb.set_trace()

		fileGroups = []

		while item_id_dict:
			key, value = item_id_dict.popitem()

			sims = self.mapMatrice.retItems(key, compThresh)
			if sims:
				tempDict = {}
				for subkey, subval in list(sims.items()):
					for other_key, other in list(item_id_dict.items()):
						if subkey == other.id_num:
							item = item_id_dict[subkey]
							tempDict[item] = subval
							if subkey in item_id_dict:
								del item_id_dict[subkey]

				tempDict[value] = "Original"

				if len(tempDict) > 1:
					fileGroups.append(tempDict)

				# raise RuntimeError

		return fileGroups

	def close(self):
		#gc seems to fail to catch the exit, resulting in lots of temp files everywhere
		self.mapMatrice.close()

class Test():
	def __init__(self):
		self.obj = Comparator()

	def go(self):
		return self.obj.comp(r"N:\IRC")#\uns2")


if __name__ == "__main__":
	sLen = len(sys.argv)
	if sLen > 1:
		if sys.argv[1] == "-t":
			s = """\
from __main__ import *
tester = Test()
			"""
			tmr = timeit.Timer("tester.go()", s)
			print(tmr)
			execs = 3
			print("%.10f sec/pass" % (tmr.timeit(number=execs) / execs))

		if sys.argv[1] == "-p":
			import cProfile
			import pstats

			tester = Test()
			cProfile.run("tester.go()", 'fooprof')

			p = pstats.Stats('fooprof')
			p.strip_dirs().sort_stats('cumulative').print_stats()

	sys.exit(0)

