# To change this template, choose Tools | Templates
# and open the template in the editor.
import os
import os.path
import Levenshtein as Lv
import numpy as np


from . import comutative_matrix
from . import filename_container
from . import config


	#def __repr__(self):
	#	return (repr((self.fn, self.cn, self.pairs)))



class Comparator():
	def __init__(self, comp_conf = None):

		if comp_conf is None:
			comp_conf = config.ConfigObj()

		self.sort_into_set = set()
		self.sort_from_set = set()
		self.map_matrice = None

		self.comp_conf = comp_conf

	def load_files(self, target_dir, files=False, dirs=False):

		assert files or dirs
		assert not(files and dirs)

		print("Getting File List of %s" % target_dir)

		dirCont = []
		if not os.access(target_dir, os.W_OK):
			print("cannot access Directory")
			return set()

		dirCont = os.listdir(target_dir)

		if not dirCont:
			print("No files in target Directory!")
			return set()

		file_id = 0
		file_set = set()
		for item in dirCont:
			item_fqp = os.path.join(target_dir, item)
			if (
					(files and os.path.isfile(item_fqp))
					or
					(dirs and os.path.isdir(item_fqp))
					):
				file_obj = filename_container.Filename(
						filename       = item,
						config         = self.comp_conf,
						id_num         = file_id,
						containing_dir = target_dir
					)
				file_set.add(file_obj)
				file_id += 1

		return file_set

	def sort_into(self, sort_from, sort_into):
		'''
		trimTree() sorts into the names in file_set,
		so we load the sort_into dir into that so it
		works without needing more custom logic.
		'''

		self.sort_into_set = self.load_files(sort_into, dirs=True)
		sort_into_count = len(self.sort_into_set)
		if not sort_into_count:
			print("No input files?", sort_into, self.sort_into_set)
			print(os.listdir(sort_into))
			return

		self.sort_from_set = self.load_files(sort_from, files=True)
		if not self.sort_from_set:
			print("No output files?")
			return

		sort_from_cnt = len(self.sort_from_set)
		if not sort_from_cnt:
			print("No output files?")
			return

		self.map_matrice = comutative_matrix.NonComutativeMatrix(
			matrix_x=sort_into_count,
			matrix_y=sort_from_cnt
			)


		for sort_into_dir in self.sort_into_set:
			for sort_from_file in self.sort_from_set:
				similarity = sort_into_dir.comp(sort_from_file)
				self.map_matrice.set(x=sort_into_dir.id_num, y=sort_from_file.id_num, val=similarity)


	def sort(self, target_dir):
		self.sort_into_set = self.load_files(target_dir, files=True)
		num_files = len(self.sort_into_set)
		if not num_files:
			return

		self.map_matrice = comutative_matrix.ComutativeMatrix(num_files)
		for target_file in self.sort_into_set:

			for comp_file in self.sort_into_set:
				if (
						target_file != comp_file
					and
						target_file.id_num >= comp_file.id_num
					):
					self.map_matrice.set(comp_file.id_num, target_file.id_num, target_file.comp(comp_file))

	def trim_into(self, compThresh):
		if not self.map_matrice:
			return []

		compThresh = float(compThresh)

		sort_into_item_id_dict = {}
		for value in self.sort_into_set:
			sort_into_item_id_dict[value.id_num] = value

		sort_from_item_id_dict = {}
		for value in self.sort_from_set:
			sort_from_item_id_dict[value.id_num] = value

		fileGroups = []

		while sort_into_item_id_dict:
			key, item = sort_into_item_id_dict.popitem()

			similar_items = self.map_matrice.get_items_greater_then(key, compThresh)
			if similar_items:
				temp_dict = {}
				for sort_from_key, similarity in similar_items.items():
					match = sort_from_item_id_dict[sort_from_key]
					match.set_dest_path(item.src_fqpath)
					temp_dict[match] = similarity

				temp_dict[item] = "Source"

				if len(temp_dict) > 1:
					fileGroups.append(temp_dict)

				# raise RuntimeError

		return fileGroups


	def trim_single(self, compThresh):
		if not self.map_matrice:
			return []

		compThresh = float(compThresh)

		item_id_dict = {}
		for value in self.sort_into_set:
			item_id_dict[value.id_num] = value

		fileGroups = []

		while item_id_dict:
			key, item = item_id_dict.popitem()
			sims = self.map_matrice.get_items_greater_then(key, compThresh)

			if sims:
				temp_dict = {}


				dest  = filename_container.Filename(
						filename       = item.cn.title(),
						config         = self.comp_conf,
						id_num         = -1,
						containing_dir = item.src_path,
					)

				temp_dict[dest] = "Source"

				for subkey, similarity in sims.items():
					for other_key, other in list(item_id_dict.items()):
						if subkey == other.id_num:
							assert other_key == subkey
							temp_dict[other] = similarity
							if subkey in item_id_dict:
								del item_id_dict[subkey]

				temp_dict[item] = "Original"


				if len(temp_dict) > 2:
					fileGroups.append(temp_dict)

				# raise RuntimeError

		return fileGroups

	def trimTree(self, compThresh):
		if self.comp_conf.enable_sort_to_dir:
			return self.trim_into(compThresh)
		else:
			return self.trim_single(compThresh)


	def close(self):
		#gc seems to fail to catch the exit, resulting in lots of temp files everywhere
		self.map_matrice.close()


