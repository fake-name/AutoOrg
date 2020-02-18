# To change this template, choose Tools | Templates
# and open the template in the editor.
import re
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

