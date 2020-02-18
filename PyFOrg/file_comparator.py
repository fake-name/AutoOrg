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
from . import comutative_matrix
from . import filename_container
from . import config


	#def __repr__(self):
	#	return (repr((self.fn, self.cn, self.pairs)))



class Comparator():
	def __init__(self, compConf = None):

		if compConf is None:
			compConf = config.ConfigObj()

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
				file = filename_container.Filename(
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

		self.mapMatrice = comutative_matrix.ComutativeMatrix(num_files)
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

