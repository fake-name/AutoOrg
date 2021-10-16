# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QMainWindow

import gui_gen
import config

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


		# self.gui.comp_threshold_slider                  .SetValue(self.config.compThreshold)
		# self.gui.slider_word_length_weighting            .SetValue(self.config.wordDifferenceWeighting)
		# self.gui.slider_str_length_difference_weighting   .SetValue(self.config.strLengthWeighting)
		# self.gui.slider_word_length_difference_weighting  .SetValue(self.config.word_length_weighting)
		# self.gui.filename_cleaner_text_ctrl                         = wx.TextCtrl(parent, -1, self.config.stripStr)
		# self.gui.text_clean_parentheses_checkbox.Value              = self.config.parentheses
		# self.gui.text_clean_brackets_checkbox.Value                 = self.config.brackets
		# self.gui.text_clean_curly_brackets_checkbox.Value            = self.config.curlyBraces
		# self.gui.start_address                               = wx.TextCtrl(parent, -1, self.config.target_dir)
		# self.gui.sort_into_dir                              = wx.TextCtrl(parent, -1, self.config.sort_to_dir)
		self.gui.enable_disable_sort_to               .setChecked(self.config.enable_sort_to_dir)


	def bind_signals(self):
		self.gui.slider_word_length_weighting           .valueChanged.connect(self.handler_word_length_weighting_adjusted)
		self.gui.slider_str_length_difference_weighting .valueChanged.connect(self.handler_str_len_difference_adjusted)
		self.gui.slider_word_length_difference_weighting.valueChanged.connect(self.handler_word_len_difference_weighting_adjusted)

		# self.Bind(wx.EVT_SCROLL_CHANGED, self.regen_notify,                           self.slider_word_length_weighting)
		# self.Bind(wx.EVT_SCROLL_CHANGED, self.regen_notify,                           self.slider_str_length_difference_weighting)
		# self.Bind(wx.EVT_SCROLL_CHANGED, self.regen_notify,                           self.slider_word_length_difference_weighting)

		# self.Bind(wx.EVT_CHECKBOX, self.update_checkboxes_config_evt,                 self.text_clean_parentheses_checkbox)
		# self.Bind(wx.EVT_CHECKBOX, self.update_checkboxes_config_evt,                 self.text_clean_brackets_checkbox)
		# self.Bind(wx.EVT_CHECKBOX, self.update_checkboxes_config_evt,                 self.text_clean_curly_brackets_checkbox)


		# self.Bind(wx.EVT_BUTTON, self.expand_tree,                                 expand_all_tree_branches_button)
		# self.Bind(wx.EVT_BUTTON, self.expand_checked_tree_items,                   expand_checked_items_button)
		# self.Bind(wx.EVT_BUTTON, self.check_all_tree_items,                        check_all_items_button)
		# self.Bind(wx.EVT_BUTTON, self.collapse_checked_tree_items,                 collapse_checked_items_button)
		# self.Bind(wx.EVT_BUTTON, self.collapse_tree,                               collapse_all_tree_branches_button)
		# self.Bind(wx.EVT_BUTTON, self.uncheck_all_tree_items,                      uncheck_all_items_button)
		# self.Bind(wx.EVT_BUTTON, self.check_items_with_threshold,                  button_check_items)
		# self.Bind(wx.EVT_BUTTON, self.move_selected_items_into_new_folders,        button_move_files)
		# self.Bind(wx.EVT_BUTTON, self.select_dir_pressed,                          select_dir_button)
		# self.Bind(wx.EVT_BUTTON, self.start_dir_processing,                        start_proc_button)

		self.handler_toggle_sort_to_evt(None)
		self.gui.enable_disable_sort_to.toggled.connect(self.handler_toggle_sort_to_evt)

		# self.Bind(wx.EVT_COMMAND_SCROLL, self.threshold_slider_adjusted, self.comp_threshold_slider)

		# self.Bind(wx.EVT_SCROLL_CHANGED, self.threshold_slider_changed,  self.comp_threshold_slider)

		# self.Bind(wx.EVT_CLOSE, self.handler_close_event)


	def handler_toggle_sort_to_evt(self, evt):
		self.config.enable_sort_to_dir = self.gui.enable_disable_sort_to.isChecked()

		if self.config.enable_sort_to_dir:
			self.gui.sort_into_dir.setEnabled(False)
			self.gui.select_sort_into_dir_button.setEnabled(False)
			self.gui.enable_disable_sort_to.setText("Enable")
		else:
			self.gui.sort_into_dir.setEnabled(True)
			self.gui.select_sort_into_dir_button.setEnabled(True)
			self.gui.enable_disable_sort_to.setText("Disable")

	def handler_word_length_weighting_adjusted(self, event):
		self.config.word_length_weighting = float(self.gui.slider_word_length_weighting.value())
		textVal = self.config.word_length_weighting/1000
		self.gui.value_word_length_weighting.setText("%0.3f" % textVal)


	def handler_str_len_difference_adjusted(self, event):
		self.config.str_length_weighting = float(self.gui.slider_str_length_difference_weighting.value())
		textVal = self.config.str_length_weighting/1000
		self.gui.value_str_length_difference_weighting.setText("%0.3f" % textVal)

	def handler_word_len_difference_weighting_adjusted(self, event):
		self.config.word_difference_weighting = float(self.gui.slider_word_length_difference_weighting.value())
		textVal = self.config.word_difference_weighting/1000
		self.gui.value_word_length_difference_weighting.setText("%0.3f" % textVal)


	def handler_select_dir_pressed(self, event):

		openFolder = wx.DirDialog (self, message = "Select Folder")
		openFolder.SetPath(self.fileSourceDir)
		if openFolder.ShowModal() == wx.ID_OK:
			path = openFolder.GetPath()

			self.startAddress.SetValue(path)
			self.config.target_dir = path

		event.Skip()

	def handler_start_dir_processing(self, event):
				#try:
		#	self.compar.close()
		#except:
		#	pass
		#the GC seems to catch and delete self.compar, unless sys.exit(0) is called

		self.fileSourceDir = self.startAddress.GetValue()
		self.config.stripTerms = self.filenameCleanerTextCtrl.Value.split(":")
		print("Stripping Terms: ", self.config.stripTerms)


		if os.access(self.fileSourceDir, os.F_OK):
			print("Path OK")
			self.compar = file_comparator.Comparator(self.config)
			self.compar.comp(self.fileSourceDir)

			self.trimmedDict = self.compar.trimTree(self.config.getCompThresh())
			print("Adding to Tree", end=' ')
			#print self.trimmedDict
			if len(self.trimmedDict) < 1:
				print("No items. Either folder is empty or thresholds are set incorrectly.")
			self.addDicttoTree(self.trimmedDict)
		else:
			print("Cannot Access Path %s" % self.fileSourceDir)

		event.Skip()


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
		openFolder.SetPath(self.fileSourceDir)
		if openFolder.ShowModal() == wx.ID_OK:
			targetDir = openFolder.GetPath()

		print(targetDir)
		mainLevel = self.treeRoot.GetChildren()

		if self.fileSourceDir is not None and mainLevel is not [None]:
			for item in self.treeRoot.GetChildren():
				if item.IsChecked():
					currWorkingDir = os.path.join(targetDir, item.GetText())
					if not os.access(currWorkingDir, os.F_OK):
						print(os.mkdir(currWorkingDir))
					for child in item.GetChildren():
						if child.IsChecked():
							fileName = child.GetData().fn
							originalFullPath = os.path.join(self.fileSourceDir, fileName)
							destFullPath = os.path.join(currWorkingDir, fileName)
							print("	", originalFullPath, end=' ')
							if os.access(originalFullPath, os.F_OK):
								print(shutil.move(originalFullPath, destFullPath))

			wx.GetApp().Yield(True)	#Yield execution to the GUI to allow printing


		print("Done moving Files")
		event.Skip()

	def handler_threshold_slider_adjusted(self, event):
		self.config.compThreshold = self.compThresholdSlider.GetValue()
		self.sliderValueLabel.setText("%s" % self.config.getCompThresh())

	def handler_update_checkboxes_config_evt(self, event):
		self.config.parentheses = self.textCleanParenthesesCheckbox.Value
		self.config.brackets = self.textCleanBracketsCheckbox.Value
		self.config.curlyBraces = self.textCleanCurlyBracketsCheckbox.Value

		event.Skip()

	def handler_threshold_slider_changed(self, event):
		try:
			assert self.compar

			self.config.compThreshold = self.compThresholdSlider.GetValue()
			print("Recomputing similarity tree")
			print("Trimming Tree")
			self.trimmedDict = self.compar.trimTree(self.config.getCompThresh())
			#print "Adding Tree"
			#print self.trimmedDict
			self.addDicttoTree(self.trimmedDict)
		except:
			print("Need to run comparison first")



	# def addTreeNodes(self, parentItem, items):

	# 	for item in items:
	# 		if isinstance(item, str):
	# 			self.fileTree.AppendItem(parentItem, item)
	# 		else:
	# 			newItem = self.fileTree.AppendItem(parentItem, item[0])
	# 			self.addTreeNodes(newItem, item)

	def addDicttoTree(self, filesList):
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

	def handler_close_event(self, event):
		print("Exiting")
		try:
			self.compar.close()
		except:
			pass
