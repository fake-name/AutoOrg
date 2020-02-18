#pylint: disable=W0201

import json
import traceback
import os
import sys
import shutil


import wx
import wx.lib.agw.customtreectrl as ctc

from . import file_comparator
from . import config


# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode


# import customtreectrl as ctc

class RedirectText:
	def __init__(self,aWxTextCtrl):
		self.out = aWxTextCtrl

	def flush(self):
		pass

	def write(self,string):
		wx.CallAfter(self.out.AppendText, ("%s" % string))

		#If you really want to print to the Console
		#sys.stderr.write("%s" % string)


ID_ABOUT = 101
ID_OPEN = 102
ID_EXIT = 103

# end wxGlade
#import traceback

class MainFrame(wx.Frame):

	fileSourceDir = ""

	filesDict = {}

	wordLengthWeighting = 1
	wordDifference = 1
	wordDifferenceWeighting = 1


	def __init__(self, *args, **kwds):
		self.config      = config.ConfigObj()
		self.compar      = None
		self.trimmedDict = None

		try:
			with open("config.json", "r") as fp:
				self.config.load(json.load(fp))
		except:
			# No config file - Using Defaults
			pass

		# begin wxGlade: MainFrame.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)

		self.SetTitle("pyFOrg - Python Automatic File Sorter and Organizer")
		self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
		self.__create_components()


	def __create_components(self):
		self.notebook                                        = wx.Notebook(self, -1, style=0)
		self.notebook.SetMinSize((1100, 520))

		self.notebookConfigPane                              = wx.Panel(self.notebook, -1)
		self.notebookFilePane                                = wx.Panel(self.notebook, -1)

		self.__create_config_pane(self.notebookConfigPane)

		self.StatusText                                      = wx.StaticText(self, -1, "Status:")


		self.__doLayout()



		self.Bind(wx.EVT_TEXT, self.checkPreprocessingRE,                         self.filenameCleanerRegexTextCtrl)
		self.Bind(wx.EVT_COMMAND_SCROLL, self.wordLengthWeightingAdjusted,        self.sliderWordLengthWeighting)
		self.Bind(wx.EVT_COMMAND_SCROLL, self.strLenDifferenceAdjusted,           self.sliderStrLengthDifferenceWeighting)
		self.Bind(wx.EVT_COMMAND_SCROLL, self.wordLenDifferenceWeightingAdjusted, self.sliderWordLengthDifferenceWeighting)


		self.compThresholdSlider                .SetValue(self.config.compThreshold)
		self.sliderWordLengthWeighting          .SetValue(self.config.wordDifferenceWeighting)
		self.sliderStrLengthDifferenceWeighting .SetValue(self.config.strLengthWeighting)
		self.sliderWordLengthDifferenceWeighting.SetValue(self.config.wordLengthWeighting)


		self.Bind(wx.EVT_SCROLL_CHANGED, self.regenNotify, self.sliderWordLengthWeighting)
		self.Bind(wx.EVT_SCROLL_CHANGED, self.regenNotify, self.sliderStrLengthDifferenceWeighting)
		self.Bind(wx.EVT_SCROLL_CHANGED, self.regenNotify, self.sliderWordLengthDifferenceWeighting)

		self.Bind(wx.EVT_CHECKBOX, self.updateCheckboxesConfigEvt, self.textCleanParenthesesCheckbox)
		self.Bind(wx.EVT_CHECKBOX, self.updateCheckboxesConfigEvt, self.textCleanBracketsCheckbox)
		self.Bind(wx.EVT_CHECKBOX, self.updateCheckboxesConfigEvt, self.textCleanCurlyBracketsCheckbox)

		self.Bind(wx.EVT_CLOSE, self.CloseEvent)

		self.thresholdSliderAdjusted(None)
		self.wordLengthWeightingAdjusted(None)
		self.strLenDifferenceAdjusted(None)
		self.wordLenDifferenceWeightingAdjusted(None)
		self.Refresh()

	def __create_file_tree_pane(self, parent):
		return fileTree

	def __create_config_pane(self, parent):
		self.configTabFilenameCleaningLabel                  = wx.StaticText(parent, -1, "Pre-Comparison Filename Processing")
		self.configTabFilenameCleaningLabel.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))

		self.configTabREFilenameCleanerHeadingLabel          = wx.StaticText(parent, -1, "Regular Expression")
		self.fillerPanel3                                    = wx.Panel(parent, -1)
		self.filenameCleanerRegexTextCtrl                    = wx.TextCtrl(parent, -1, "")
		self.regexValidLabel                                 = wx.StaticText(parent, -1, "1.00")
		self.regexDocLabel                                   = wx.StaticText(parent, -1, "This RE is run on the filenames before they are compared. If you need to strip out some common factor from the filenames you're processing, do it here.\nNote: All numbers, underscores, dashes, dots, common file extensions, and any words of 2 characters or less in length are already removed without user intervention.")
		self.fillerPanel4                                    = wx.Panel(parent, -1)
		self.configTabFilenameCleanerHeadingStaticText       = wx.StaticText(parent, -1, "Text Strip List")
		self.fillerPanel3_copy                               = wx.Panel(parent, -1)

		self.filenameCleanerTextCtrl                         = wx.TextCtrl(parent, -1, self.config.stripStr)

		self.stripListValidLabel                             = wx.StaticText(parent, -1, "1.00")
		self.stripListDocLabel                               = wx.StaticText(parent, -1, "Colon (:) separated list of terms to remove from filenames before comparing. Case insensitive. \nNote: Be certain to not leave any spurious spaces, they may disrupt text removal.")
		self.fillerPanel4_copy                               = wx.Panel(parent, -1)
		self.configTabFilenameCleanerBracketRemvalStaticText = wx.StaticText(parent, -1, "Strip out text in:")

		self.textCleanParenthesesCheckbox                    = wx.CheckBox(parent, -1, "Parentheses - ()")
		self.textCleanBracketsCheckbox                       = wx.CheckBox(parent, -1, "Square Brackets - []")
		self.textCleanCurlyBracketsCheckbox                  = wx.CheckBox(parent, -1, "Curly Braces - {}")

		self.confingTabCompEngineLabel                       = wx.StaticText(parent, -1, "Comparison Engine Variables")
		self.confingTabCompEngineLabel.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))

		self.labelWordLengthWeighting                        = wx.StaticText(parent, -1, "Word Length Weighting")
		self.fillerPanel6                                    = wx.Panel(parent, -1)
		self.sliderWordLengthWeighting                       = wx.Slider(parent, -1, 1, 1, 5000, style=wx.SL_HORIZONTAL|wx.SL_TOP)
		self.valueWordLengthWeighting                        = wx.StaticText(parent, -1, "1.000")
		self.labelStrLengthDifferenceWeighting               = wx.StaticText(parent, -1, "String Length Diffreence Weighting")
		self.fillerPanel7                                    = wx.Panel(parent, -1)
		self.sliderStrLengthDifferenceWeighting              = wx.Slider(parent, -1, 1, 1, 5000, style=wx.SL_HORIZONTAL|wx.SL_TOP)
		self.valueStrLengthDifferenceWeighting               = wx.StaticText(parent, -1, "1.000")
		self.labelWordLengthDifferenceWeighting              = wx.StaticText(parent, -1, "Word Length Difference Weighting")
		self.fillerPanel8                                    = wx.Panel(parent, -1)
		self.sliderWordLengthDifferenceWeighting             = wx.Slider(parent, -1, 1, 1, 5000, style=wx.SL_HORIZONTAL|wx.SL_TOP)
		self.valueWordLengthDifferenceWeighting              = wx.StaticText(parent, -1, "1.00")
		self.settingInstructions                             = wx.StaticText(parent, -1, "All settings except the Similarity Grouping Threshold require a new comparison to be run to incorporate value changes.")

		self.textCleanParenthesesCheckbox.Value              = self.config.parentheses
		self.textCleanBracketsCheckbox.Value                 = self.config.brackets
		self.textCleanCurlyBracketsCheckbox.Value            = self.config.curlyBraces

	def __create_control_items_buttons(self, parent):

		expandAllTreeBranchesButton                     = wx.Button(parent, -1, "Expand Tree")
		expandCheckedItemsButton                        = wx.Button(parent, -1, "Expand Checked")
		checkAllItemsButton                             = wx.Button(parent, -1, "Check All")
		collapseCheckedItemsButton                      = wx.Button(parent, -1, "Collapse Checked")
		collapseAllTreeBranchesButton                   = wx.Button(parent, -1, "Collapse Tree")
		uncheckAllItemsButton                           = wx.Button(parent, -1, "Uncheck All")

		sizerControlItemsButtons = wx.GridSizer(2, 3, 0, 0)
		sizerControlItemsButtons.Add(expandAllTreeBranchesButton,   0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
		sizerControlItemsButtons.Add(expandCheckedItemsButton,      0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
		sizerControlItemsButtons.Add(checkAllItemsButton,           0, wx.EXPAND,                                                         0)
		sizerControlItemsButtons.Add(collapseAllTreeBranchesButton, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
		sizerControlItemsButtons.Add(collapseCheckedItemsButton,    0, wx.EXPAND,                                                         0)
		sizerControlItemsButtons.Add(uncheckAllItemsButton,         0, wx.EXPAND,                                                         0)

		self.Bind(wx.EVT_BUTTON, self.expandTree,               expandAllTreeBranchesButton)
		self.Bind(wx.EVT_BUTTON, self.expandCheckedTreeItems,   expandCheckedItemsButton)
		self.Bind(wx.EVT_BUTTON, self.checkAllTreeItems,        checkAllItemsButton)
		self.Bind(wx.EVT_BUTTON, self.collapseCheckedTreeItems, collapseCheckedItemsButton)
		self.Bind(wx.EVT_BUTTON, self.collapseTree,             collapseAllTreeBranchesButton)
		self.Bind(wx.EVT_BUTTON, self.uncheckAllTreeItems,      uncheckAllItemsButton)

		return sizerControlItemsButtons

	def __make_file_panel_ops_component(self, parent):
		filler_panel_1                = wx.Panel(parent, -1)
		filler_panel_2                = wx.Panel(parent, -1)
		filePaneFileOpsLabel1         = wx.StaticText(parent, -1, "Check all items with at least", style=wx.ALIGN_CENTRE)
		filePaneFileOpsLabel2         = wx.StaticText(parent, -1, "items in group.")
		buttonMoveFiles               = wx.Button(parent, -1, "Move selected files into Directory (Opens Folder Picker)")
		buttonCheckItems              = wx.Button(parent, -1, "Check Items")
		self.sliderNumFileforChecking = wx.Slider(parent, -1, 2, 2, 10, style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_RIGHT|wx.SL_TOP)

		filler_panel_1.SetMinSize((20, 50))
		filler_panel_2.SetMinSize((20,50))

		filePaneOperationsSizer = wx.BoxSizer(wx.HORIZONTAL)
		filePaneOperationsSizer.Add(filePaneFileOpsLabel1, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
		filePaneOperationsSizer.Add(self.sliderNumFileforChecking, 0, 0, 0)
		filePaneOperationsSizer.Add(filePaneFileOpsLabel2, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
		filePaneOperationsSizer.Add(buttonCheckItems, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		filePaneOperationsSizer.Add(filler_panel_1, 0, 0, 0)
		filePaneOperationsSizer.Add(self.__create_control_items_buttons(parent), 0, wx.EXPAND, 0)
		filePaneOperationsSizer.Add(filler_panel_2, 1, wx.EXPAND, 0)
		filePaneOperationsSizer.Add(buttonMoveFiles, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		self.Bind(wx.EVT_BUTTON, self.checkItemsWithThreshold, buttonCheckItems)
		self.Bind(wx.EVT_BUTTON, self.moveSelectedItemsIntoNewFolders,            buttonMoveFiles)

		return filePaneOperationsSizer

	def __create_title_sizer(self, parent):
		targetDirectoryLabel                            = wx.StaticText(parent, -1, "Directory to Process:")
		self.startAddress                               = wx.TextCtrl(parent, -1, self.config.target_dir)
		selectDirButton                                 = wx.Button(parent, -1, "Select Directory")
		titleStaticLine                                 = wx.StaticLine(parent, -1, style=wx.LI_VERTICAL)
		startProcButton                                 = wx.Button(parent, -1, "Start")


		titleSizer = wx.BoxSizer(wx.VERTICAL)
		titleSizer.Add(targetDirectoryLabel, 0, wx.ALL, 5)

		dirTextBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
		dirTextBoxSizer.Add(self.startAddress, 1, wx.EXPAND, 0)
		dirTextBoxSizer.Add(selectDirButton, 0, wx.LEFT, 5)
		dirTextBoxSizer.Add(titleStaticLine, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
		dirTextBoxSizer.Add(startProcButton, 0, 0, 0)

		titleSizer.Add(dirTextBoxSizer, 1, wx.EXPAND, 0)

		self.Bind(wx.EVT_BUTTON, self.selectDirPressed,        selectDirButton)
		self.Bind(wx.EVT_BUTTON, self.startDirProcessing,      startProcButton)

		return titleSizer

	def __create_tree_pane_sizer(self, parent):
		generalSimSliderLabel    = wx.StaticText(parent, -1, "Similarity Grouping Threshold")

		self.fileTree            = ctc.CustomTreeCtrl(parent, -1, style=ctc.TR_HAS_BUTTONS|ctc.TR_MULTIPLE|ctc.TR_AUTO_CHECK_CHILD|wx.TR_HIDE_ROOT)
		self.fileTree.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Courier New"))

		fillerPanel              = wx.Panel(parent, -1)
		self.compThresholdSlider = wx.Slider(parent, -1, 1, 1, 5000, style=wx.SL_HORIZONTAL|wx.SL_TOP)
		self.sliderValueLabel    = wx.StaticText(parent, -1, "1.00")


		# begin wxGlade: MainFrame.__do_layout
		mainOptionsGridSizer = wx.FlexGridSizer(2, 2, 0, 0)
		mainOptionsGridSizer = wx.FlexGridSizer(2, 2, 0, 0)

		mainOptionsGridSizer.Add(generalSimSliderLabel, 0, 0, 0)
		mainOptionsGridSizer.Add(fillerPanel, 1, wx.EXPAND, 0)
		mainOptionsGridSizer.Add(self.compThresholdSlider, 0, wx.EXPAND, 0)
		mainOptionsGridSizer.Add(self.sliderValueLabel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
		mainOptionsGridSizer.AddGrowableCol(0)

		notebookTreeSizer = wx.BoxSizer(wx.VERTICAL)
		notebookTreeSizer.Add(self.fileTree, 1, wx.EXPAND, 0)
		notebookTreeSizer.Add(mainOptionsGridSizer, 0, wx.ALL|wx.EXPAND, 10)
		notebookTreeSizer.Add(self.__make_file_panel_ops_component(self.notebookFilePane), 0, wx.EXPAND, 0)

		self.Bind(wx.EVT_COMMAND_SCROLL, self.thresholdSliderAdjusted,            self.compThresholdSlider)
		self.Bind(wx.EVT_SCROLL_CHANGED, self.thresholdSliderChanged, self.compThresholdSlider)

		return notebookTreeSizer

	def __doLayout(self):

		self.notebookFilePane.SetSizer(self.__create_tree_pane_sizer(self.notebookFilePane))

		configTabFilenameRECleanerGridSizer = wx.FlexGridSizer(3, 2, 0, 0)
		configTabFilenameRECleanerGridSizer.Add(self.configTabREFilenameCleanerHeadingLabel, 0, 0, 0)
		configTabFilenameRECleanerGridSizer.Add(self.fillerPanel3, 1, wx.EXPAND, 0)
		configTabFilenameRECleanerGridSizer.Add(self.filenameCleanerRegexTextCtrl, 0, wx.EXPAND, 0)
		configTabFilenameRECleanerGridSizer.Add(self.regexValidLabel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
		configTabFilenameRECleanerGridSizer.Add(self.regexDocLabel, 0, 0, 0)
		configTabFilenameRECleanerGridSizer.Add(self.fillerPanel4, 1, wx.EXPAND, 0)
		configTabFilenameRECleanerGridSizer.AddGrowableCol(0)

		configTabFilenameCleanerGridSizer = wx.FlexGridSizer(3, 2, 0, 0)
		configTabFilenameCleanerGridSizer.Add(self.configTabFilenameCleanerHeadingStaticText, 0, 0, 0)
		configTabFilenameCleanerGridSizer.Add(self.fillerPanel3_copy, 1, wx.EXPAND, 0)
		configTabFilenameCleanerGridSizer.Add(self.filenameCleanerTextCtrl, 0, wx.EXPAND, 0)
		configTabFilenameCleanerGridSizer.Add(self.stripListValidLabel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
		configTabFilenameCleanerGridSizer.Add(self.stripListDocLabel, 0, 0, 0)
		configTabFilenameCleanerGridSizer.Add(self.fillerPanel4_copy, 1, wx.EXPAND, 0)
		configTabFilenameCleanerGridSizer.AddGrowableCol(0)

		textStripEnclosingItemCheckboxesSizer = wx.BoxSizer(wx.HORIZONTAL)
		textStripEnclosingItemCheckboxesSizer.Add(self.configTabFilenameCleanerBracketRemvalStaticText, 0, 0, 0)
		textStripEnclosingItemCheckboxesSizer.Add(self.textCleanParenthesesCheckbox, 0, wx.LEFT|wx.RIGHT, 5)
		textStripEnclosingItemCheckboxesSizer.Add(self.textCleanBracketsCheckbox, 0, 0, 0)
		textStripEnclosingItemCheckboxesSizer.Add(self.textCleanCurlyBracketsCheckbox, 0, wx.LEFT|wx.RIGHT, 5)

		configTabFilenameCleanerSizer = wx.BoxSizer(wx.VERTICAL)
		configTabFilenameCleanerSizer.Add(self.configTabFilenameCleaningLabel, 0, wx.ALL, 3)
		configTabFilenameCleanerSizer.Add(configTabFilenameRECleanerGridSizer, 0, wx.ALL|wx.EXPAND, 10)
		configTabFilenameCleanerSizer.Add(configTabFilenameCleanerGridSizer, 0, wx.ALL|wx.EXPAND, 10)
		configTabFilenameCleanerSizer.Add(textStripEnclosingItemCheckboxesSizer, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)

		specialOptionsGridSizer = wx.FlexGridSizer(6, 2, 0, 0)
		specialOptionsGridSizer.Add(self.labelWordLengthWeighting, 0, 0, 0)
		specialOptionsGridSizer.Add(self.fillerPanel6, 1, wx.EXPAND, 0)
		specialOptionsGridSizer.Add(self.sliderWordLengthWeighting, 0, wx.EXPAND, 0)
		specialOptionsGridSizer.Add(self.valueWordLengthWeighting, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
		specialOptionsGridSizer.Add(self.labelStrLengthDifferenceWeighting, 0, wx.TOP, 10)
		specialOptionsGridSizer.Add(self.fillerPanel7, 1, wx.EXPAND, 0)
		specialOptionsGridSizer.Add(self.sliderStrLengthDifferenceWeighting, 0, wx.EXPAND, 0)
		specialOptionsGridSizer.Add(self.valueStrLengthDifferenceWeighting, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
		specialOptionsGridSizer.Add(self.labelWordLengthDifferenceWeighting, 0, wx.TOP, 10)
		specialOptionsGridSizer.Add(self.fillerPanel8, 1, wx.EXPAND, 0)
		specialOptionsGridSizer.Add(self.sliderWordLengthDifferenceWeighting, 0, wx.EXPAND, 0)
		specialOptionsGridSizer.Add(self.valueWordLengthDifferenceWeighting, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
		specialOptionsGridSizer.AddGrowableCol(0)

		configTabCompEngineSlidersSizer = wx.BoxSizer(wx.VERTICAL)
		configTabCompEngineSlidersSizer.Add(self.confingTabCompEngineLabel, 0, wx.ALL, 3)
		configTabCompEngineSlidersSizer.Add(specialOptionsGridSizer, 0, wx.ALL|wx.EXPAND, 10)

		configTabMainSizer = wx.BoxSizer(wx.VERTICAL)
		configTabMainSizer.Add(configTabFilenameCleanerSizer, 0, wx.EXPAND, 0)
		configTabMainSizer.Add(configTabCompEngineSlidersSizer, 1, wx.EXPAND, 0)
		configTabMainSizer.Add(self.settingInstructions, 0, wx.ALL, 5)

		self.notebookConfigPane.SetSizer(configTabMainSizer)
		self.notebook.AddPage(self.notebookFilePane, "File List")
		self.notebook.AddPage(self.notebookConfigPane, "Settings")

		MainSizer = wx.BoxSizer(wx.VERTICAL)
		MainSizer.Add(self.__create_title_sizer(self), 0, wx.EXPAND, 0)
		MainSizer.Add(self.notebook, 1, wx.EXPAND, 0)
		MainSizer.Add(self.StatusText, 0, wx.ALL, 5)
		self.SetSizer(MainSizer)
		MainSizer.Fit(self)
		self.Layout()


		# sys.stdout = redir
		# sys.sterr  = redir

		self.treeRoot = self.fileTree.AddRoot("All")

		# end wxGlade

	def selectDirPressed(self, event): # wxGlade: MainFrame.<event_handler>


		openFolder = wx.DirDialog (self, message = "Select Folder")
		openFolder.SetPath(self.fileSourceDir)
		if openFolder.ShowModal() == wx.ID_OK:
			path = openFolder.GetPath()

			self.startAddress.SetValue(path)
			self.config.target_dir = path

		event.Skip()

	def startDirProcessing(self, event): # wxGlade: MainFrame.<event_handler>

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

	def checkItemsWithThreshold(self, event): # wxGlade: MainFrame.<event_handler>
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

	def expandTree(self, event): # wxGlade: MainFrame.<event_handler>
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			item.Expand()

		#self.notebookFilePane.Update()
		self.notebookFilePane.Refresh()
		self.fileTree.EnsureVisible(self.treeRoot)	#IF you don't have this, the scroll bar in on the treectrl won't appear untill you manually change the size ov one of the items in it.
		#self.Update()
		#self.Refresh()

		event.Skip()

	def collapseTree(self, event): # wxGlade: MainFrame.<event_handler>
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			item.Collapse()

		#self.notebookFilePane.Update()
		self.notebookFilePane.Refresh()
		self.fileTree.EnsureVisible(self.treeRoot)	#IF you don't have this, the scroll bar in on the treectrl won't appear untill you manually change the size ov one of the items in it.
		#self.Update()
		#self.Refresh()

		event.Skip()

	def checkAllTreeItems(self, event): # wxGlade: MainFrame.<event_handler>
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			#print item.GetText()
			item.Check()
			for child in item.GetChildren():
				child.Check()

		self.Refresh()
		event.Skip()

	def uncheckAllTreeItems(self, event): # wxGlade: MainFrame.<event_handler>
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			#print item.GetText()
			item.Check(False)
			for child in item.GetChildren():
				child.Check(False)
		self.Refresh()
		event.Skip()

	def collapseCheckedTreeItems(self, event):
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			if item.IsChecked():
				item.Collapse()

		#self.notebookFilePane.Update()
		self.notebookFilePane.Refresh()
		self.fileTree.EnsureVisible(self.treeRoot)	#IF you don't have this, the scroll bar in on the treectrl won't appear untill you manually change the size ov one of the items in it.
		#self.Update()
		#self.Refresh()

		event.Skip()

	def expandCheckedTreeItems(self, event):
		mainLevel = self.treeRoot.GetChildren()
		#print mainLevel
		for item in mainLevel:
			if item.IsChecked():
				item.Expand()

		#self.notebookFilePane.Update()
		self.notebookFilePane.Refresh()
		self.fileTree.EnsureVisible(self.treeRoot)	#IF you don't have this, the scroll bar in on the treectrl won't appear untill you manually change the size ov one of the items in it.
		#self.Update()
		#self.Refresh()
		event.Skip()

	def moveSelectedItemsIntoNewFolders(self, event): # wxGlade: MainFrame.<event_handler>
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

	def checkPreprocessingRE(self, event): # wxGlade: MainFrame.<event_handler>
		print("Whoops - Regular expressions are not yet implemented")
		event.Skip()

	def thresholdSliderAdjusted(self, event): # wxGlade: MainFrame.<event_handler>
		self.config.compThreshold = self.compThresholdSlider.GetValue()
		self.sliderValueLabel.SetLabel("%s" % self.config.getCompThresh())

	def updateCheckboxesConfigEvt(self, event): # wxGlade: MainFrame.<event_handler>
		self.config.parentheses = self.textCleanParenthesesCheckbox.Value
		self.config.brackets = self.textCleanBracketsCheckbox.Value
		self.config.curlyBraces = self.textCleanCurlyBracketsCheckbox.Value

		event.Skip()

	def thresholdSliderChanged(self, event): # wxGlade: MainFrame.<event_handler>
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


	def wordLengthWeightingAdjusted(self, event): # wxGlade: MainFrame.<event_handler>
		self.config.wordLengthWeighting = float(self.sliderWordLengthWeighting.GetValue())

		textVal = self.config.wordLengthWeighting/1000

		self.valueWordLengthWeighting.SetLabel("%s" % textVal)


	def strLenDifferenceAdjusted(self, event): # wxGlade: MainFrame.<event_handler>
		self.config.strLengthWeighting = float(self.sliderStrLengthDifferenceWeighting.GetValue())

		textVal = self.config.strLengthWeighting/1000

		self.valueStrLengthDifferenceWeighting.SetLabel("%s" % textVal)



	def wordLenDifferenceWeightingAdjusted(self, event): # wxGlade: MainFrame.<event_handler>
		self.config.wordDifferenceWeighting = float(self.sliderWordLengthDifferenceWeighting.GetValue())

		textVal = self.config.wordDifferenceWeighting/1000

		self.valueWordLengthDifferenceWeighting.SetLabel("%s" % textVal)




	def addTreeNodes(self, parentItem, items):

		for item in items:
			if isinstance(item, str):
				self.fileTree.AppendItem(parentItem, item)
			else:
				newItem = self.fileTree.AppendItem(parentItem, item[0])
				self.addTreeNodes(newItem, item)

	def addDicttoTree(self, filesList):
		self.fileTree.DeleteChildren(self.treeRoot)
		fnLen = 0
		cnLen = 0
		for group in filesList:
			#print "Group"
			#print group.keys()[0].cn
			#thisBranch = self.fileTree.AppendItem(self.treeRoot, group.keys()[0].cn.title(), ct_type=1)

			for itemdict, simVal in group.items():
				tLen = len(itemdict.fn)
				if tLen > fnLen:
					fnLen = tLen
				tLen = len(itemdict.cn)
				if tLen > cnLen:
					cnLen = tLen
		for group in filesList:
			#print "Group"
			#print group.keys()[0].cn
			thisBranch = self.fileTree.AppendItem(self.treeRoot, list(group.keys())[0].cn.title(), ct_type=1)

			for itemdict, simVal in list(group.items()):
				self.fileTree.AppendItem(thisBranch, "Cleaned String - : %s : - Original String - : %s  : - Similarity Metric Value: %s" % (itemdict.cn.ljust(cnLen+1), itemdict.fn.ljust(fnLen+1), simVal), ct_type=1, data=itemdict)
				#print self.fileTree.SetPyData(leafID, (itemdict, simVal))
				#print "	", itemdict.fn
			#print fnLen, cnLen
		try:
			self.treeRoot.Expand()
		except:
			pass

		print(" - Done")

	def regenNotify(self, event):
		print("Note: you must rerun the file comparison to update results with new comparion coefficents")

	def CloseEvent(self, event):
		print("Exiting")
		try:
			self.compar.close()
		except:
			pass

		self.config.target_dir = self.startAddress.GetValue()
		self.config.stripStr = self.filenameCleanerTextCtrl.Value
		#print self.config
		with open("config.json", "w") as fp:
			conf = json.dumps(
				self.config.dump(),
				indent = 4
				)
			fp.write(conf)

		sys.exit()
	# end of class MainFrame
