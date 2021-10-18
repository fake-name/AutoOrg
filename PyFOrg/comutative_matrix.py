

import os.path
import tempfile

import numpy as np
import h5py


class ComutativeMatrix:
	# Matrix of simlarity values
	# Setting array[fileid_num1, fileid_num2] = simVal adds item to array
	# reading is accomplished by x = array[fileid_num1, fileid_num2]
	# since the similarity between two items is commutative ( array[fileid_num1, fileid_num2] ==  array[fileid_num2, fileid_num1] ),
	# if we always sort the arguments passed through __getattr__ so the larger one is first, reduncancy should be eliminated
	# Therefore The order which you pass items, both to read and write is not important
	# It should store the minimum ammount of information to hold the entirety of all comparison items

	# This is oooooooooold, old enough that the original implementation was done on 32-bit windows
	# XP (and python.....2.5, I think?). I had lots of issues with the 32-bit memory limit, which
	# is why there's the ability to use a h5py memory-mapped onto a file.
	# It let me exceed the memory limits of a 32-bit process.

	def __init__(self, matrixSz):
		self.matrixSz = matrixSz

		if matrixSz > 5000:
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
			self.m = np.zeros((matrixSz, matrixSz))

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



