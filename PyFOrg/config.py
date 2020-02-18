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



	#def __repr__(self):
	#	return (repr((self.fn, self.cn, self.pairs)))

class ConfigObj(object):
	def __init__(self):
		self.compThreshold           = 1500

		self.wordLengthWeighting     = 1000
		self.strLengthWeighting      = 1000
		self.wordDifferenceWeighting = 1000

		self.stripTerms              = []
		self.stripStr                = ""

		self.brackets                = True
		self.parentheses             = True
		self.curlyBraces             = True

		self.mappingDict             = {}
		self.target_dir              = "~/"


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



