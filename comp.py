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

try:
	import psyco
	psyco.full()
except:
	#No PsyCo, Can't do anything about that....
	pass

def compStr(strA, strB):
	sLAt = strA.split(" ")
	sLBt = strB.split(" ")
	
	lenSLAt = len(sLAt)
	lenSLBt = len(sLBt)
	
	
	if lenSLAt < lenSLBt:
		sLA = sLAt
		sLB = sLBt
		lenSLA = lenSLAt
		lenSLB = lenSLBt
	else:
		sLA = sLBt
		sLB = sLAt
		lenSLA = lenSLBt
		lenSLB = lenSLAt

	#compConfDict - {"wordDifference" : 1.00, "wordLengthWeighting" : 1.00, "wordDifferenceWeighting" : 1.00}

	totalSim = 0
	
	for x in range(lenSLA):				#The magic (or obsfucation, take your pick)
		if (len(sLA[x]) > 1):
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
						#pprint([sLA, sLB, sLA[x], sLB[y], wordSimilarity, wordWeight])
			if wordWeight > 0:
				totalSim += wordSimilarity * math.sqrt(wordWeight)

	#print sLA, sLB, strA, strB
	divRatio = lenSLA if lenSLA > lenSLB else lenSLB
	if divRatio == 0:
		print totalSim, divRatio
		return 0
	return(totalSim / divRatio)

class Filename:

	gid = None
	sim = None

	def __init__(self, filename, config, idNo):

		self.idNo = idNo

		#print "PreClean", filename
		tempCleaned = filename
		if config.brackets:
			tempCleaned = re.sub("\[.*?\]", " ", tempCleaned)
		if config.parentheses:
			tempCleaned = re.sub("\(.*?\)", " ", tempCleaned)
		if config.curlyBraces:
			tempCleaned = re.sub("\{.*?\}", " ", tempCleaned)

		#print "PostClean", tempCleaned
		tempCleaned = re.sub("'", "", tempCleaned)
		#remove punctuation cleanly (')apostrophes

		tempCleaned = re.sub("\.rar|\.zip|\.cbr|\.cbz|\.7z|\.jpg|\.png", " ", tempCleaned, re.IGNORECASE)	#remove known file suffixes
		tempCleaned = re.sub("([\[\]_\+0-9()=!,])", " ", tempCleaned)				#clean brackets, symbols, and numbers: Removed "-"
		tempCleaned = re.sub("\W(ch|vol)[0-9]+?", " ", tempCleaned)				#Clean 'ch01' or similar
		tempCleaned = re.sub("\W[vc][0-9]*?\W", " ", tempCleaned)				#Clean 'v01' and 'c01' or similar
		tempCleaned = re.sub("\W[a-zA-z0-9]\W", " ", tempCleaned)				#Remove all single letters
		
		for term in config.stripTerms:
			#print "Term ", term
			tempRE = re.compile(term, re.IGNORECASE)
			tempCleaned = tempRE.sub(" ", tempCleaned)
		
		tempCleaned = re.sub("\.", " ", tempCleaned).lower()					#Remove dots
		tempCleaned = re.sub(" +", " ", tempCleaned).rstrip().lstrip()				#reduce all repeated spaces to one space

		self.fn = filename
		self.cn = tempCleaned
		
		
	def __repr__(self):
		return "'Filename Item for %s'\n	cleanedName = %s\n	simVal = %s\n	groupID = %s\n" % (self.fn, self.cn, self.sim, self.gid)

	def comp(self, otherFile):
		compValue = compStr(self.cn, otherFile.cn)
		return compValue
		#compConf.mapMatrice[otherFile.idNo, self.idNo] = compValue
			

	def purge(self, sMatrix, thresh = 1.3):
		for key, value in self.pairs.items():
			if value < thresh:
				del self.pairs[key]
				#print "removed key", value, thresh
				#print type(value), type(thresh)
				#print value, thresh, value < thresh
				#print "Deling Key", key.fn



	#def __repr__(self):
	#	return (repr((self.fn, self.cn, self.pairs)))

class ConfigObj:
	compThreshold			=	1500

	wordLengthWeighting		=	1000
	strLengthWeighting		=	1000
	wordDifferenceWeighting		=	1000

	stripTerms			=	[]
	stripStr			=	"by twilight dreams scans:senfgurke:chapter:volume:season"

	brackets	=	True
	parentheses	=	True
	curlyBraces	=	True

	mappingDict	=	{}

	def getCompThresh(self):
		return float(self.compThreshold)/1000

	def dump(self):
		config = {}
		config["compThreshold"] = self.compThreshold

		config["wordLengthWeighting"] = self.wordLengthWeighting
		config["strLengthWeighting"] = self.strLengthWeighting
		config["wordDifferenceWeighting	"] = self.wordDifferenceWeighting

		config["stripTerms"] = self.stripTerms
		config["stripStr"] = self.stripStr

		config["brackets"] = self.brackets
		config["parentheses"] = self.parentheses
		config["curlyBraces"] = self.curlyBraces

		return config
	
	def load(self, config):
		
		self.compThreshold = config["compThreshold"]

		self.wordLengthWeighting = config["wordLengthWeighting"]
		self.strLengthWeightingconfig = config["strLengthWeighting"]
		self.wordDifferenceWeighting = config["wordDifferenceWeighting	"]

		self.stripTerms = config["stripTerms"]
		self.stripStr = config["stripStr"]

		self.brackets = config["brackets"]
		self.parentheses = config["parentheses"]
		self.curlyBraces = config["curlyBraces"]
		
		return

class oneMatrix:
	#Matrix of simlarity values
	#Setting array[fileIDNO1, fileIDNO2] = simVal adds item to array
	#reading is accomplished by x = array[fileIDNO1, fileIDNO2]
	#since the similarity between two items is commutative ( array[fileIDNO1, fileIDNO2] ==  array[fileIDNO2, fileIDNO1] ),
	#if we always sort the arguments passed through __getattr__ so the larger one is first, reduncancy should be eliminated

	#Therefore The order which you pass items, both to read and write is not important

	#It should store the minimum ammount of information to hold the entirety of all comparison items
	
	def __init__(self, matrixSz):
		self.matrixSz = matrixSz
		
		if matrixSz > 5000:
			print
			self.mmapped = True
			self.tempF = tempfile.mkstemp()
			self.f = h5py.File(self.tempF[1], 'w')

			self.m = self.f.create_dataset('ds', (matrixSz,matrixSz), compression='gzip', compression_opts=4)
			
			print "Initializing Array Tempfile - \"%s\"" % self.tempF[1]
			if matrixSz > 5000:
				print "This could take a while"
			#self.m[:] = -1		#Broadcast array to -1
			print "Array Initialized"
			#print self.m[:]
			#print self.m.items()
		else:
			print "Using in-memory array"
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

	def addRow(self, index, rowDat):
		self.m[index,...] = rowDat

	def retItems(self, key, thresh):
		#print thresh
		out = {}
		xRang = self.m[...,key]
		yRang = self.m[key,...]
		for value in range(self.matrixSz):
			sim = xRang[value] if xRang[value] > yRang[key] else yRang[key]
			if sim > thresh and value != key: out[value] = sim
			#print self.m[value,key], self.m[key,value], sim
		return out

	def __del__(self):
		if self.mmapped:
			try:
				self.f.close()
			except:
				print "Could not close database file due to an unknown reason"
				print "This error may be caused by excessive disk activity"
				pass
			try:
				os.close(self.tempF[0])
			except:
				print "Could not close pipe"
				print "This error may be caused by excessive disk activity"
				pass
			try:
				os.unlink(self.tempF[1])
			except:
				print "Could not delete temporary database file at - %s" % self.tempF[1], "due to an unknown error"
				print "You may want to delete it manually"
				print "This error may be caused by excessive disk activity"
				pass
	def close(self):
		self.__del__()
		

class Comparator:
	def __init__(self, compConf = ConfigObj, printDebug=False):
		self.compConf = compConf
		self.debug = printDebug

	def comp(self, targetDir):

		
		print "Getting File List..."

		wx.GetApp().Yield()	#Yield execution to the GUI to allow printing

		files = []
		dirCont = []
		if os.access(targetDir, os.W_OK):
			dirCont = os.listdir(targetDir)
		else:
			print "cannot access Directory"

		#if self.debug:
		#print "File List Size = %s" % asizeof(dirCont)
		numFiles = len(dirCont)
		#print dirCont
		if numFiles == 0:
			print "No files in target Directory!"
			return

		wx.GetApp().Yield()	#Yield execution to the GUI to allow printing
		#Import list of file names, and push them into a dictionary
		print "Number of Files = %s" % numFiles
		print "Scrubbing File Names of Dirs"
		count = 0
		self.fileDict = {}
		self.compConf.itemDict = {}
		for item in dirCont:
			if os.path.isfile(os.path.join(targetDir, item)):
				file = Filename(item, self.compConf, count)
				files.append(file)
				self.compConf.itemDict[count] = file
				self.fileDict[file.fn] = file
				if count % 250 == 0:
					print "File %s of %s" % (count, numFiles)
					wx.GetApp().Yield()	#Yield execution to the GUI to allow printing
				count += 1

		#print "File List Size = %s" % asizeof(files)
		#raw_input("Press enter to continue")
		print "Starting Comparison"
		files.sort()
		#print files


		#print self.fileDict
		loopctr = 0

		#print "%s" % spCl


		self.compConf.mapMatrice = oneMatrix(numFiles)
		#print  self.fileDict
		for targetKey, targetFile in self.fileDict.items():
			

			subArr = np.zeros((numFiles))

			for compKey, compFile in self.fileDict.items():
				if targetFile != compFile:
					if not targetFile.idNo < compFile.idNo:
						
						subArr[compFile.idNo] = targetFile.comp(compFile)

			self.compConf.mapMatrice.addRow(targetFile.idNo, subArr)

			loopctr += 1
			#print "Size = %s" % asizeof(targetFile),
			#print " Len of pairs = %s" % len(targetFile.pairs)
			#if self.debug:

			#Print **more** for lots of files, because each step takes longer
			#This makes progress more visible
			if numFiles < 1000: modu = 25
			elif numFiles < 5000: modu = 10
			else: modu = 1

			if loopctr % modu == 0:
				print "Step:", loopctr,
				print " - Remaning steps:", numFiles - loopctr
				wx.GetApp().Yield()	#Yield execution to the GUI to allow printing

		print "Done Comparison"
		print "Operation required %s string comparisons" % (numFiles*(numFiles-1)/2)
		#print self.compConf.mapMatrice
		
		if self.debug:
			for key, value in self.compConf.itemDict.items():
				print key, value.fn, "comped to: "
				for tkey, tvalue in self.compConf.itemDict.items():
					if tkey != key:
						print "	", tkey, tvalue.fn, tvalue.cn
				#for subkey, subval in value.pairs.items():
				#	print "	", subkey.fn, subval

		#mx = self.compConf.mapMatrice.m
		#print mx[:]

	def trimTree(self, compThresh = 1.5):

		compThresh = float(compThresh)

		inFileDict = {}

		for key, value in self.fileDict.items():
			#print "Item -----", value.fn, value.idNo
			inFileDict[value.idNo] = value

		

		fileGroups = []
		#print compThresh
		#print inFileDict
		retList = False
		if retList:
			#For when/if I switch the comp engine over to an ObjectListView
		
			while len(inFileDict) > 0:
				value = inFileDict.popitem()
				#if self.debug:
				#print value,
				#print value[1].fn
				sims = self.compConf.mapMatrice.retItems(value[0], compThresh)
				#print value
				#print sims
				#print inFileDict
				gid = value[1].cn.rstrip().lstrip()

				if len(sims)> 0:

					#print "sims", sims

					for subkey, subval in sims.items():
						if subkey in inFileDict:
							item = inFileDict[subkey]
							item.sim = subval
							item.gid = gid
							fileGroups.append(item)
							#print subkey
							if subkey in inFileDict:
								#print "Deling ", subkey
								del inFileDict[subkey]
					value[1].sim = "Original"
					value[1].gid = gid
					fileGroups.append(value[1])
					print item.fn, "Has Items!"



						#print "appended"

				#print "remaining Files - ", len(inFileDict)
				#print value[1].fn, value[0]

		else:
			while len(inFileDict) > 0:
				value = inFileDict.popitem()
				#if self.debug:
				#print value,
				#print value[1].fn
				sims = self.compConf.mapMatrice.retItems(value[0], compThresh)
				#print value
				#print sims
				#print inFileDict
				if len(sims)> 0:
					tempDict = {}
					#print "sims", sims

					for subkey, subval in sims.items():
						if subkey in inFileDict:
							item = inFileDict[subkey]
							tempDict[item] = subval
							#print subkey
							if subkey in inFileDict:
								#print "Deling ", subkey
								del inFileDict[subkey]
					tempDict[value[1]] = "Original"

					print len(inFileDict), "Files Remaining - ",
					print "%s Has %s Items!" % (item.fn, len(tempDict))

					if len(tempDict) > 1:
						fileGroups.append(tempDict)

					wx.GetApp().Yield()	#Yield execution to the GUI to allow printing
						#print "appended"

				#print "remaining Files - ", len(inFileDict)
				#print value[1].fn, value[0]

		
		#print fileGroups
		return fileGroups

	def close(self):
		#gc seems to fail to catch the exit, resulting in lots of temp files everywhere
		self.compConf.mapMatrice.close()

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
			print tmr
			execs = 3
			print "%.10f sec/pass" % (tmr.timeit(number=execs) / execs)

		if sys.argv[1] == "-p":
			import cProfile
			import pstats

			tester = Test()
			cProfile.run("tester.go()", 'fooprof')

			p = pstats.Stats('fooprof')
			p.strip_dirs().sort_stats('cumulative').print_stats()

	sys.exit(0)

	