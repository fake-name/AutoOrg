# This Python file uses the following encoding: utf-8
import shutil
import os
import json
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QMainWindow

from . import gui_gen
from . import config
from . import file_comparator

class PyFOrg(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)


		main_widget = QWidget()
		self.gui = gui_gen.Ui_MainWidget()
		self.gui.setupUi(main_widget)

		self.setCentralWidget(main_widget)

		self.load_config()

		self.bind_signals()

	def load_config(self):

		self.config      = config.ConfigObj()
		try:
			with open("config.json", "r") as fp:
				self.config.load(json.load(fp))
		except:
			# No config file - Using Defaults
			pass


		self.gui.comp_threshold_slider                    .setValue(self.config.comp_threshold)
		self.gui.slider_word_length_weighting             .setValue(self.config.word_length_weighting)
		self.gui.slider_str_length_difference_weighting   .setValue(self.config.str_length_weighting)
		self.gui.slider_word_length_difference_weighting  .setValue(self.config.word_difference_weighting)


		self.gui.filename_cleaner_text_ctrl               .setText(self.config.strip_str)
		self.gui.sort_source_location                     .setText(self.config.sort_from_dir)
		self.gui.sort_into_dir                            .setText(self.config.sort_to_dir)

		self.gui.enable_disable_sort_to                   .setChecked(self.config.enable_sort_to_dir)

		self.gui.text_clean_parentheses_checkbox          .setChecked(self.config.parentheses)
		self.gui.text_clean_brackets_checkbox             .setChecked(self.config.brackets)
		self.gui.text_clean_curly_brackets_checkbox       .setChecked(self.config.curly_braces)


		# Update the labels
		self.handler_threshold_slider_adjusted(None)
		self.handler_word_length_weighting_adjusted(None)
		self.handler_str_len_difference_adjusted(None)
		self.handler_word_len_difference_weighting_adjusted(None)

	def bind_signals(self):
		self.gui.slider_word_length_weighting           .valueChanged.connect(self.handler_word_length_weighting_adjusted)
		self.gui.slider_str_length_difference_weighting .valueChanged.connect(self.handler_str_len_difference_adjusted)
		self.gui.slider_word_length_difference_weighting.valueChanged.connect(self.handler_word_len_difference_weighting_adjusted)

		self.gui.text_clean_parentheses_checkbox   .stateChanged.connect(self.handler_update_checkboxes_config_evt)
		self.gui.text_clean_brackets_checkbox      .stateChanged.connect(self.handler_update_checkboxes_config_evt)
		self.gui.text_clean_curly_brackets_checkbox.stateChanged.connect(self.handler_update_checkboxes_config_evt)


		self.gui.expand_tree                .clicked.connect(self.handler_expand_tree)
		self.gui.expand_checked_tree_items  .clicked.connect(self.handler_expand_checked_tree_items)
		self.gui.check_all_tree_items       .clicked.connect(self.handler_check_all_tree_items)
		self.gui.collapse_checked_tree_items.clicked.connect(self.handler_collapse_checked_tree_items)
		self.gui.collapse_tree              .clicked.connect(self.handler_collapse_tree)
		self.gui.uncheck_all_tree_items     .clicked.connect(self.handler_uncheck_all_tree_items)

		self.gui.button_check_items         .clicked.connect(self.handler_check_items_with_threshold)

		self.gui.button_move_files          .clicked.connect(self.handler_move_selected_items_into_new_folders)
		self.gui.start_proc_button          .clicked.connect(self.handler_start_dir_processing)

		self.gui.select_dir_button          .clicked.connect(self.handler_select_source_dir_pressed)
		self.gui.select_sort_into_dir_button.clicked.connect(self.handler_select_target_dir_pressed)

		self.handler_toggle_sort_to_evt(None)
		self.gui.enable_disable_sort_to.toggled.connect(self.handler_toggle_sort_to_evt)

		self.gui.comp_threshold_slider.valueChanged.connect(self.handler_threshold_slider_adjusted)
		self.gui.comp_threshold_slider.sliderReleased.connect(self.handler_threshold_slider_changed)


	def handler_select_source_dir_pressed(self, _event):

		new_folder = QFileDialog.getExistingDirectory(self,
			caption = 'Select source directory to sort',
			dir = self.config.sort_from_dir)
		if new_folder:
			self.gui.sort_source_location.setText(new_folder)
			self.config.sort_from_dir = new_folder

	def handler_select_target_dir_pressed(self, _event):

		new_folder = QFileDialog.getExistingDirectory(self,
			caption = 'Select target directory to sort into',
			dir = self.config.sort_to_dir)
		if new_folder:
			self.gui.sort_into_dir.setText(new_folder)
			self.config.sort_to_dir = new_folder


	def handler_toggle_sort_to_evt(self, _event):
		self.config.enable_sort_to_dir = self.gui.enable_disable_sort_to.isChecked()

		if self.config.enable_sort_to_dir:
			self.gui.sort_into_dir.setEnabled(False)
			self.gui.select_sort_into_dir_button.setEnabled(False)
			self.gui.enable_disable_sort_to.setText("Enable")
		else:
			self.gui.sort_into_dir.setEnabled(True)
			self.gui.select_sort_into_dir_button.setEnabled(True)
			self.gui.enable_disable_sort_to.setText("Disable")

	def handler_word_length_weighting_adjusted(self, _event):
		self.config.word_length_weighting = float(self.gui.slider_word_length_weighting.value())
		textVal = self.config.word_length_weighting/1000
		self.gui.value_word_length_weighting.setText("%0.3f" % textVal)


	def handler_str_len_difference_adjusted(self, _event):
		self.config.str_length_weighting = float(self.gui.slider_str_length_difference_weighting.value())
		textVal = self.config.str_length_weighting/1000
		self.gui.value_str_length_difference_weighting.setText("%0.3f" % textVal)

	def handler_word_len_difference_weighting_adjusted(self, _event):
		self.config.word_difference_weighting = float(self.gui.slider_word_length_difference_weighting.value())
		textVal = self.config.word_difference_weighting/1000
		self.gui.value_word_length_difference_weighting.setText("%0.3f" % textVal)



	def handler_threshold_slider_adjusted(self, _event):
		self.config.comp_threshold = self.gui.comp_threshold_slider.value()
		self.gui.com_threshold_slider_value_label.setText("%0.3f" % self.config.getCompThresh())

	def handler_update_checkboxes_config_evt(self, _event):
		self.config.parentheses  = self.gui.text_clean_parentheses_checkbox   .isChecked()
		self.config.brackets     = self.gui.text_clean_brackets_checkbox      .isChecked()
		self.config.curly_braces = self.gui.text_clean_curly_brackets_checkbox.isChecked()

	def handler_threshold_slider_changed(self):
		try:
			assert self.compar

			self.config.compThreshold = self.compThresholdSlider.GetValue()
			print("Recomputing similarity tree")
			print("Trimming Tree")
			self.trimmed_dict = self.compar.trimTree(self.config.getCompThresh())
			#print "Adding Tree"
			#print self.trimmed_dict
			self.add_dict_to_tree(self.trimmed_dict)
		except:
			print("Need to run comparison first")


	def closeEvent(self, event):
		print("Exiting")
		try:
			self.compar.close()
		except:
			pass


		self.config.strip_str   = self.gui.filename_cleaner_text_ctrl.text()
		self.config.sort_from_dir  = self.gui.sort_source_location.text()
		self.config.sort_to_dir = self.gui.sort_into_dir.text()


		with open("config.json", "w") as fp:
			conf = json.dumps(
				self.config.dump(),
				indent = 4
				)
			fp.write(conf)

			event.accept()

	def handler_start_dir_processing(self, event):
				#try:
		#	self.compar.close()
		#except:
		#	pass
		#the GC seems to catch and delete self.compar, unless sys.exit(0) is called

		file_source_dir = self.gui.sort_source_location.text()
		terms = self.gui.filename_cleaner_text_ctrl.text().split(":")
		terms = [tmp for tmp in terms if tmp]
		self.config.strip_terms = terms
		print("Stripping Terms: ", self.config.strip_terms)


		if os.access(file_source_dir, os.F_OK):
			print("Path OK")
			self.compar = file_comparator.Comparator(self.config)
			self.compar.comp(file_source_dir)

			self.trimmed_dict = self.compar.trimTree(self.config.getCompThresh())
			print("Adding to Tree", end=' ')
			#print self.trimmed_dict
			if len(self.trimmed_dict) < 1:
				print("No items. Either folder is empty or thresholds are set incorrectly.")
			self.add_dict_to_tree(self.trimmed_dict)
		else:
			print("Cannot Access Path %s" % file_source_dir)

		event.Skip()

	# ----------------------------------------------
	# To Update




	def handler_check_items_with_threshold(self, event):
		mainLevel = self.treeRoot.GetChildren()
		sliderVal = self.sliderNumFileforChecking.GetValue()
		for item in mainLevel:
			print(item.GetText())
			childNum = len(item.GetChildren())
			if childNum >= sliderVal:
				item.Check()
				for child in item.GetChildren():
					child.Check()
			else:
				item.Check(False)
				for child in item.GetChildren():
					child.Check(False)
			print("has %s children" % childNum)
			#wx.GetApp().Yield()	#Yield execution to the GUI to allow printing

		self.Refresh()
		event.Skip()

	def handler_expand_tree(self, event):
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			item.Expand()

		#self.notebookFilePane.Update()
		self.notebookFilePane.Refresh()

		#IF you don't have this, the scroll bar in on the treectrl won't appear untill you manually change the size of one of the items in it.
		self.fileTree.EnsureVisible(self.treeRoot)

		#self.Update()
		#self.Refresh()

		event.Skip()

	def handler_collapse_tree(self, event):
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			item.Collapse()

		#self.notebookFilePane.Update()
		self.notebookFilePane.Refresh()

		#IF you don't have this, the scroll bar in on the treectrl won't appear untill you manually change the size of one of the items in it.
		self.fileTree.EnsureVisible(self.treeRoot)

		#self.Update()
		#self.Refresh()

		event.Skip()

	def handler_check_all_tree_items(self, event):
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			#print item.GetText()
			item.Check()
			for child in item.GetChildren():
				child.Check()

		self.Refresh()
		event.Skip()

	def handler_uncheck_all_tree_items(self, event):
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			#print item.GetText()
			item.Check(False)
			for child in item.GetChildren():
				child.Check(False)
		self.Refresh()
		event.Skip()

	def handler_collapse_checked_tree_items(self, event):
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			if item.IsChecked():
				item.Collapse()

		#self.notebookFilePane.Update()
		self.notebookFilePane.Refresh()

		#IF you don't have this, the scroll bar in on the treectrl won't appear untill you manually change the size of one of the items in it.
		self.fileTree.EnsureVisible(self.treeRoot)

		#self.Update()
		#self.Refresh()

		event.Skip()

	def handler_expand_checked_tree_items(self, event):
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			if item.IsChecked():
				item.Expand()

		#self.notebookFilePane.Update()
		self.notebookFilePane.Refresh()

		#IF you don't have this, the scroll bar in on the treectrl won't appear untill you manually change the size of one of the items in it.
		self.fileTree.EnsureVisible(self.treeRoot)

		#self.Update()
		#self.Refresh()
		event.Skip()

	def handler_move_selected_items_into_new_folders(self, event):
		openFolder = wx.DirDialog (self, message = "Select Folder")
		openFolder.SetPath(self.file_source_dir)
		if openFolder.ShowModal() == wx.ID_OK:
			targetDir = openFolder.GetPath()

		print(targetDir)
		mainLevel = self.treeRoot.GetChildren()

		if self.file_source_dir is not None and mainLevel is not [None]:
			for item in self.treeRoot.GetChildren():
				if item.IsChecked():
					currWorkingDir = os.path.join(targetDir, item.GetText())
					if not os.access(currWorkingDir, os.F_OK):
						print(os.mkdir(currWorkingDir))
					for child in item.GetChildren():
						if child.IsChecked():
							fileName = child.GetData().fn
							originalFullPath = os.path.join(self.file_source_dir, fileName)
							destFullPath = os.path.join(currWorkingDir, fileName)
							print("	", originalFullPath, end=' ')
							if os.access(originalFullPath, os.F_OK):
								print(shutil.move(originalFullPath, destFullPath))

			wx.GetApp().Yield(True)	#Yield execution to the GUI to allow printing


		print("Done moving Files")
		event.Skip()

	# def addTreeNodes(self, parentItem, items):

	# 	for item in items:
	# 		if isinstance(item, str):
	# 			self.fileTree.AppendItem(parentItem, item)
	# 		else:
	# 			newItem = self.fileTree.AppendItem(parentItem, item[0])
	# 			self.addTreeNodes(newItem, item)

	def add_dict_to_tree(self, filesList):
		self.fileTree.DeleteChildren(self.treeRoot)
		fnLen = 0
		cnLen = 0
		for group in filesList:
			#thisBranch = self.fileTree.AppendItem(self.treeRoot, group.keys()[0].cn.title(), ct_type=1)

			for itemdict, simVal in group.items():
				tLen_1 = len(itemdict.fn)
				if tLen_1 > fnLen:
					fnLen = tLen_1
				tLen_2 = len(itemdict.cn)
				if tLen_2 > cnLen:
					cnLen = tLen_2

		for group in filesList:
			#print "Group"
			#print group.keys()[0].cn
			thisBranch = self.fileTree.AppendItem(self.treeRoot, list(group.keys())[0].cn.title(), ct_type=1)

			fnLen = 0
			cnLen = 0
			for itemdict, simVal in group.items():
				tLen_1 = len(itemdict.fn)
				if tLen_1 > fnLen:
					fnLen = tLen_1
				tLen_2 = len(itemdict.cn)
				if tLen_2 > cnLen:
					cnLen = tLen_2

			for itemdict, simVal in list(group.items()):
				self.fileTree.AppendItem(thisBranch, "Cleaned String - : %s : - Original String - : %s  : - Similarity Metric Value: %s" %
						(
							itemdict.cn.ljust(cnLen+1),
							itemdict.fn.ljust(fnLen+1),
							simVal
						),
					ct_type=1, data=itemdict)
				#print self.fileTree.SetPyData(leafID, (itemdict, simVal))
				#print "	", itemdict.fn
			#print fnLen, cnLen
		try:
			self.treeRoot.Expand()
		except:
			pass

		print(" - Done")

	def handler_regen_notify(self, event):
		print("Note: you must rerun the file comparison to update results with new comparion coefficents")


