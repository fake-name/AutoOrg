# To change this template, choose Tools | Templates
# and open the template in the editor.
import os.path
import tempfile
import Levenshtein as Lv
import numpy as np

import h5py
from . import filename_container
from . import config


class NonComutativeMatrix(object):

	def __init__(self, matrix_x, matrix_y):
		self.matrix_x = matrix_x
		self.matrix_y = matrix_y

		cells = self.matrix_x * self.matrix_y

		if cells > 250_000_000:
			self.mmapped = True
			self.tempF = tempfile.mkstemp()
			self.f = h5py.File(self.tempF[1], 'w')

			self.m = self.f.create_dataset('ds', (self.matrix_x, self.matrix_y), compression='gzip', compression_opts=4)

			print("Initializing Array Tempfile - \"%s\"" % self.tempF[1])
			if cells > 250_000_000:
				print("This could take a while")
			#self.m[:] = -1		#Broadcast array to -1
			print("Array Initialized")
			#print self.m[:]
			#print self.m.items()
		else:
			print("Using in-memory array")
			self.mmapped = False
			self.m = np.zeros((self.matrix_x, self.matrix_y))

	def get(self, x, y):
		return self.m[x, y]

	def set(self, x, y, val):
		self.m[x, y] = val

	def get_items_greater_then(self, key_x, thresh):
		#print thresh
		out = {}
		xRang = self.m[key_x, ...]
		matrix_sz = len(xRang)
		for idx in range(matrix_sz):
			sim = xRang[idx]
			if sim > thresh:
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



class ComutativeMatrix(object):
	# Matrix of simlarity values
	# Setting array[fileid_num1, fileid_num2] = simVal adds item to array
	# reading is accomplished by x = array[fileid_num1, fileid_num2]
	# since the similarity between two items is commutative ( array[fileid_num1, fileid_num2] ==  array[fileid_num2, fileid_num1] ),
	# if we always sort the arguments passed through __getattr__ so the larger one is first, reduncancy should be eliminated
	# Therefore The order which you pass items, both to read and write is not important
	# It should store the minimum ammount of information to hold the entirety of all comparison items

	def __init__(self, matrix_sz):
		self.matrix_sz = matrix_sz
		cells = matrix_sz * matrix_sz
		if cells > 250_000_000:
			print()
			self.mmapped = True
			self.tempF = tempfile.mkstemp()
			self.f = h5py.File(self.tempF[1], 'w')

			self.m = self.f.create_dataset('ds', (matrix_sz, matrix_sz), compression='gzip', compression_opts=4)

			print("Initializing Array Tempfile - \"%s\"" % self.tempF[1])
			if cells > 250_000_000:
				print("This could take a while")
			#self.m[:] = -1		#Broadcast array to -1
			print("Array Initialized")
			#print self.m[:]
			#print self.m.items()
		else:
			print("Using in-memory array")
			self.mmapped = False
			self.m = np.zeros((matrix_sz, matrix_sz))

	def get(self, x, y):
		if x <= y:
			return self.m[x, y]
		else:
			return self.m[y, x]

	def set(self, x, y, val):
		if x <= y:
			self.m[x, y] = val
		else:
			self.m[y, x] = val

	def get_items_greater_then(self, key, thresh):
		#print thresh
		out = {}
		xRang = self.m[...,key]
		yRang = self.m[key,...]
		for idx in range(self.matrix_sz):
			sim = xRang[idx] if xRang[idx] > yRang[key] else yRang[key]
			if sim > thresh:
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



