# To change this template, choose Tools | Templates
# and open the template in the editor.
import re
import os.path
import math
import Levenshtein as Lv
import timeit
import numpy as np


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

	def __init__(self, filename, config, id_num, containing_dir):

		print("Comparing:", filename)
		self.similarity_cache = None

		self.__id_no = id_num

		#print "PreClean", filename
		temp_cleaned = filename
		if config.brackets:
			temp_cleaned = re.sub(r"\[.*?\]", " ", temp_cleaned)
		if config.parentheses:
			temp_cleaned = re.sub(r"\(.*?\)", " ", temp_cleaned)
		if config.curly_braces:
			temp_cleaned = re.sub(r"\{.*?\}", " ", temp_cleaned)

		#print "PostClean", temp_cleaned
		temp_cleaned = re.sub("'", "", temp_cleaned)
		#remove punctuation cleanly (')apostrophes

		temp_cleaned = re.sub(r"\.rar|\.zip|\.cbr|\.cbz|\.7z|\.jpg|\.png", " ", temp_cleaned, re.IGNORECASE)	#remove known file suffixes
		temp_cleaned = re.sub(r"([\[\]_\+0-9()=!,])", " ", temp_cleaned)				#clean brackets, symbols, and numbers: Removed "-"
		temp_cleaned = re.sub(r"\W(ch|vol)[0-9]+?", " ", temp_cleaned)				#Clean 'ch01' or similar
		temp_cleaned = re.sub(r"\W[vc][0-9]*?\W", " ", temp_cleaned)				#Clean 'v01' and 'c01' or similar
		temp_cleaned = re.sub(r"\W[a-zA-z0-9]\W", " ", temp_cleaned)				#Remove all single letters

		for term in [t for t in config.strip_terms if t]:
			tempRE = re.compile(term, re.IGNORECASE)
			temp_cleaned = tempRE.sub(" ", temp_cleaned)

		temp_cleaned = re.sub(r"\.", " ", temp_cleaned).lower()					#Remove dots
		temp_cleaned = re.sub(r" +", " ", temp_cleaned).rstrip().lstrip()				#reduce all repeated spaces to one space

		self.fn = filename
		self.cn = temp_cleaned
		self.__src_path = containing_dir
		self.__dest_path = None

	@property
	def src_path(self):
		return os.path.normpath(self.__src_path)

	@property
	def dest_path(self):
		return os.path.normpath(self.__dest_path)

	@property
	def src_fqpath(self):
		return os.path.normpath(os.path.join(self.__src_path, self.fn))

	@property
	def dest_fqpath(self):
		return os.path.normpath(os.path.join(self.__dest_path, self.fn))

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


	def comp(self, other_file):
		comp_value = compStr(self.cn, other_file.cn)
		return comp_value
		#compConf.mapMatrice[other_file.id_num, self.id_num] = comp_value

	def set_dest_path(self, fpath):
		print("Set dest path:", fpath)
		self.__dest_path = fpath

