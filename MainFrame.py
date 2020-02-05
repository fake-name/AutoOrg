# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Sat Apr 10 00:13:40 2010

import wx
import customtreectrl as ctc

#import ObjectListView as olv
#import other

import pickle

import os

import comp



# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
import sys
import shutil

class RedirectText:
	def __init__(self,aWxTextCtrl):
		self.out=aWxTextCtrl

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

	config = comp.ConfigObj()

	def __init__(self, *args, **kwds):

		try:
			pickleFile = open("config.pik", "r")
			self.config = comp.ConfigObj()
			self.config.load(pickle.load(pickleFile))
			#print self.config
			#print self.config.dump()
			pickleFile.close()
			#print "Loaded Config"
		except:
			#traceback.print_exc()
			print "No config file - Using Defaults"
			self.config = None
			self.config = comp.ConfigObj()
			pass

		# begin wxGlade: MainFrame.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.notebook = wx.Notebook(self, -1, style=0)
		self.notebookConfigPane = wx.Panel(self.notebook, -1)
		self.notebookFilePane = wx.Panel(self.notebook, -1)
		self.targetDirectoryLabel = wx.StaticText(self, -1, "Directory to Process:")
		self.startAddress = wx.TextCtrl(self, -1, r"N:\Comics\Unsorted\absolution")
		self.selectDirButton = wx.Button(self, -1, "Select Directory")
		self.titleStaticLine = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
		self.startProcButton = wx.Button(self, -1, "Start")
		self.fileTree = ctc.CustomTreeCtrl(self.notebookFilePane, -1, style=ctc.TR_HAS_BUTTONS|ctc.TR_MULTIPLE|ctc.TR_AUTO_CHECK_CHILD|wx.TR_HIDE_ROOT)
		self.generalSimSliderLabel = wx.StaticText(self.notebookFilePane, -1, "Similarity Grouping Threshold")
		self.fillerPanel5 = wx.Panel(self.notebookFilePane, -1)
		self.compThresholdSlider = wx.Slider(self.notebookFilePane, -1, 1, 1, 5000, style=wx.SL_HORIZONTAL|wx.SL_TOP)
		self.sliderValueLabel = wx.StaticText(self.notebookFilePane, -1, "1.00")
		self.filePaneFileOpsLabel1 = wx.StaticText(self.notebookFilePane, -1, "Check all items with at least", style=wx.ALIGN_CENTRE)
		self.sliderNumFileforChecking = wx.Slider(self.notebookFilePane, -1, 2, 2, 10, style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_RIGHT|wx.SL_TOP)
		self.filePaneFileOpsLabel2 = wx.StaticText(self.notebookFilePane, -1, "items in group.")
		self.buttonCheckItems = wx.Button(self.notebookFilePane, -1, "Check Items")
		self.fillerPanel1 = wx.Panel(self.notebookFilePane, -1)

		self.expandAllTreeBranchesButton = wx.Button(self.notebookFilePane, -1, "Expand Tree")
		self.collapseAllTreeBranchesButton = wx.Button(self.notebookFilePane, -1, "Collapse Tree")

		self.expandCheckedItemsButton = wx.Button(self.notebookFilePane, -1, "Expand Checked")
		self.collapseCheckedItemsButton = wx.Button(self.notebookFilePane, -1, "Collapse Checked")

		self.checkAllItemsButton = wx.Button(self.notebookFilePane, -1, "Check All")
		self.uncheckAllItemsButton = wx.Button(self.notebookFilePane, -1, "Uncheck All")

		self.fillerPanel2 = wx.Panel(self.notebookFilePane, -1)
		self.buttonMoveFiles = wx.Button(self.notebookFilePane, -1, "Move selected files into Directory (Opens Folder Picker)")
		self.configTabFilenameCleaningLabel = wx.StaticText(self.notebookConfigPane, -1, "Pre-Comparison Filename Processing")
		self.configTabREFilenameCleanerHeadingLabel = wx.StaticText(self.notebookConfigPane, -1, "Regular Expression")
		self.fillerPanel3 = wx.Panel(self.notebookConfigPane, -1)
		self.filenameCleanerRegexTextCtrl = wx.TextCtrl(self.notebookConfigPane, -1, "")
		self.regexValidLabel = wx.StaticText(self.notebookConfigPane, -1, "1.00")
		self.regexDocLabel = wx.StaticText(self.notebookConfigPane, -1, "This RE is run on the filenames before they are compared. If you need to strip out some common factor from the filenames you're processing, do it here.\nNote: All numbers, underscores, dashes, dots, common file extensions, and any words of 2 characters or less in length are already removed without user intervention.")
		self.fillerPanel4 = wx.Panel(self.notebookConfigPane, -1)
		self.configTabFilenameCleanerHeadingStaticText = wx.StaticText(self.notebookConfigPane, -1, "Text Strip List")
		self.fillerPanel3_copy = wx.Panel(self.notebookConfigPane, -1)
		try:
			self.filenameCleanerTextCtrl = wx.TextCtrl(self.notebookConfigPane, -1, self.config.stripStr)
		except:
			print "Configuration File Corrupted"
			print "Defaulting to default settings"
			self.config = comp.ConfigObj
			self.filenameCleanerTextCtrl = wx.TextCtrl(self.notebookConfigPane, -1, "")


		self.stripListValidLabel = wx.StaticText(self.notebookConfigPane, -1, "1.00")
		self.stripListDocLabel = wx.StaticText(self.notebookConfigPane, -1, "Colon (:) separated list of terms to remove from filenames before comparing. Case insensitive. \nNote: Be certain to not leave any spurious spaces, they may disrupt text removal.")
		self.fillerPanel4_copy = wx.Panel(self.notebookConfigPane, -1)
		self.configTabFilenameCleanerBracketRemvalStaticText = wx.StaticText(self.notebookConfigPane, -1, "Strip out text in:")

		self.textCleanParenthesesCheckbox = wx.CheckBox(self.notebookConfigPane, -1, "Parentheses - ()")
		self.textCleanParenthesesCheckbox.Value = self.config.parentheses
		self.textCleanBracketsCheckbox = wx.CheckBox(self.notebookConfigPane, -1, "Square Brackets - []")
		self.textCleanBracketsCheckbox.Value = self.config.brackets
		self.textCleanCurlyBracketsCheckbox = wx.CheckBox(self.notebookConfigPane, -1, "Curly Braces - {}")
		self.textCleanCurlyBracketsCheckbox.Value = self.config.curlyBraces

		self.confingTabCompEngineLabel = wx.StaticText(self.notebookConfigPane, -1, "Comparison Engine Variables")
		self.labelWordLengthWeighting = wx.StaticText(self.notebookConfigPane, -1, "Word Length Weighting")
		self.fillerPanel6 = wx.Panel(self.notebookConfigPane, -1)
		self.sliderWordLengthWeighting = wx.Slider(self.notebookConfigPane, -1, 1, 1, 5000, style=wx.SL_HORIZONTAL|wx.SL_TOP)
		self.valueWordLengthWeighting = wx.StaticText(self.notebookConfigPane, -1, "1.000")
		self.labelStrLengthDifferenceWeighting = wx.StaticText(self.notebookConfigPane, -1, "String Length Diffreence Weighting")
		self.fillerPanel7 = wx.Panel(self.notebookConfigPane, -1)
		self.sliderStrLengthDifferenceWeighting = wx.Slider(self.notebookConfigPane, -1, 1, 1, 5000, style=wx.SL_HORIZONTAL|wx.SL_TOP)
		self.valueStrLengthDifferenceWeighting = wx.StaticText(self.notebookConfigPane, -1, "1.000")
		self.labelWordLengthDifferenceWeighting = wx.StaticText(self.notebookConfigPane, -1, "Word Length Difference Weighting")
		self.fillerPanel8 = wx.Panel(self.notebookConfigPane, -1)
		self.sliderWordLengthDifferenceWeighting = wx.Slider(self.notebookConfigPane, -1, 1, 1, 5000, style=wx.SL_HORIZONTAL|wx.SL_TOP)
		self.valueWordLengthDifferenceWeighting = wx.StaticText(self.notebookConfigPane, -1, "1.00")
		self.settingInstructions = wx.StaticText(self.notebookConfigPane, -1, "All settings except the Similarity Grouping Threshold require a new comparison to be run to incorporate value changes.")
		self.statusWindow = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.StatusText = wx.StaticText(self, -1, "Status:")

		self.__setProperties()
		self.__doLayout()

		self.openFolder = wx.DirDialog (self, message = "Select Folder")



		self.Bind(wx.EVT_BUTTON, self.selectDirPressed, self.selectDirButton)
		self.Bind(wx.EVT_BUTTON, self.startDirProcessing, self.startProcButton)
		self.Bind(wx.EVT_BUTTON, self.checkItemsWithThreshold, self.buttonCheckItems)
		self.Bind(wx.EVT_BUTTON, self.expandTree, self.expandAllTreeBranchesButton)
		self.Bind(wx.EVT_BUTTON, self.collapseTree, self.collapseAllTreeBranchesButton)

		self.Bind(wx.EVT_BUTTON, self.checkAllTreeItems, self.checkAllItemsButton)
		self.Bind(wx.EVT_BUTTON, self.uncheckAllTreeItems, self.uncheckAllItemsButton)

		self.Bind(wx.EVT_BUTTON, self.expandCheckedTreeItems, self.expandCheckedItemsButton)
		self.Bind(wx.EVT_BUTTON, self.collapseCheckedTreeItems, self.collapseCheckedItemsButton)


		self.Bind(wx.EVT_BUTTON, self.moveSelectedItemsIntoNewFolders, self.buttonMoveFiles)
		self.Bind(wx.EVT_TEXT, self.checkPreprocessingRE, self.filenameCleanerRegexTextCtrl)
		self.Bind(wx.EVT_COMMAND_SCROLL, self.thresholdSliderAdjusted, self.compThresholdSlider)
		self.Bind(wx.EVT_COMMAND_SCROLL, self.wordLengthWeightingAdjusted, self.sliderWordLengthWeighting)
		self.Bind(wx.EVT_COMMAND_SCROLL, self.strLenDifferenceAdjusted, self.sliderStrLengthDifferenceWeighting)
		self.Bind(wx.EVT_COMMAND_SCROLL, self.wordLenDifferenceWeightingAdjusted, self.sliderWordLengthDifferenceWeighting)

		self.Bind(wx.EVT_SCROLL_CHANGED, self.thresholdSliderChanged, self.compThresholdSlider)

		self.compThresholdSlider.SetValue(self.config.compThreshold)
		self.sliderWordLengthWeighting.SetValue(self.config.wordDifferenceWeighting)
		self.sliderStrLengthDifferenceWeighting.SetValue(self.config.strLengthWeighting)
		self.sliderWordLengthDifferenceWeighting.SetValue(self.config.wordLengthWeighting)


		self.Bind(wx.EVT_SCROLL_CHANGED, self.regenNotify, self.sliderWordLengthWeighting)
		self.Bind(wx.EVT_SCROLL_CHANGED, self.regenNotify, self.sliderStrLengthDifferenceWeighting)
		self.Bind(wx.EVT_SCROLL_CHANGED, self.regenNotify, self.sliderWordLengthDifferenceWeighting)

		self.Bind(wx.EVT_CHECKBOX, self.updateCheckboxesConfigEvt, self.textCleanParenthesesCheckbox)
		self.Bind(wx.EVT_CHECKBOX, self.updateCheckboxesConfigEvt, self.textCleanBracketsCheckbox)
		self.Bind(wx.EVT_CHECKBOX, self.updateCheckboxesConfigEvt, self.textCleanCurlyBracketsCheckbox)

		self.Bind(wx.EVT_CLOSE, self.handleExit)


		#final init:
		self.thresholdSliderAdjusted(None)
		self.wordLengthWeightingAdjusted(None)
		self.strLenDifferenceAdjusted(None)
		self.wordLenDifferenceWeightingAdjusted(None)
		self.Refresh()
		# end wxGlade

	def __setProperties(self):
		# begin wxGlade: MainFrame.__set_properties
		self.SetTitle("pyFOrg - Python Automatic File Sorter and Organizer")
		self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE))
		self.fillerPanel1.SetMinSize((20, 50))
		self.fillerPanel2.SetMinSize((20,50))
		self.configTabFilenameCleaningLabel.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
		self.confingTabCompEngineLabel.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
		self.fileTree.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Courier New"))
		self.statusWindow.SetMinSize((920, 120))
		self.notebook.SetMinSize((1100, 520))
		# end wxGlade

	def __doLayout(self):
		# begin wxGlade: MainFrame.__do_layout
		MainSizer = wx.BoxSizer(wx.VERTICAL)
		configTabMainSizer = wx.BoxSizer(wx.VERTICAL)
		configTabCompEngineSlidersSizer = wx.BoxSizer(wx.VERTICAL)
		specialOptionsGridSizer = wx.FlexGridSizer(6, 2, 0, 0)
		mainOptionsGridSizer = wx.FlexGridSizer(2, 2, 0, 0)
		configTabFilenameCleanerSizer = wx.BoxSizer(wx.VERTICAL)
		textStripEnclosingItemCheckboxesSizer = wx.BoxSizer(wx.HORIZONTAL)
		configTabFilenameCleanerGridSizer = wx.FlexGridSizer(3, 2, 0, 0)
		configTabFilenameRECleanerGridSizer = wx.FlexGridSizer(3, 2, 0, 0)
		notebookTreeSizer = wx.BoxSizer(wx.VERTICAL)
		mainOptionsGridSizer = wx.FlexGridSizer(2, 2, 0, 0)
		titleSizer = wx.BoxSizer(wx.VERTICAL)
		dirTextBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
		titleSizer.Add(self.targetDirectoryLabel, 0, wx.ALL, 5)
		dirTextBoxSizer.Add(self.startAddress, 1, wx.EXPAND, 0)
		dirTextBoxSizer.Add(self.selectDirButton, 0, wx.LEFT, 5)
		dirTextBoxSizer.Add(self.titleStaticLine, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
		dirTextBoxSizer.Add(self.startProcButton, 0, 0, 0)
		titleSizer.Add(dirTextBoxSizer, 1, wx.EXPAND, 0)
		MainSizer.Add(titleSizer, 0, wx.EXPAND, 0)
		notebookTreeSizer.Add(self.fileTree, 1, wx.EXPAND, 0)
		mainOptionsGridSizer.Add(self.generalSimSliderLabel, 0, 0, 0)
		mainOptionsGridSizer.Add(self.fillerPanel5, 1, wx.EXPAND, 0)
		mainOptionsGridSizer.Add(self.compThresholdSlider, 0, wx.EXPAND, 0)
		mainOptionsGridSizer.Add(self.sliderValueLabel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
		mainOptionsGridSizer.AddGrowableCol(0)
		notebookTreeSizer.Add(mainOptionsGridSizer, 0, wx.ALL|wx.EXPAND, 10)

		filePaneOperationsSizer = wx.BoxSizer(wx.HORIZONTAL)
		filePaneOperationsSizer.Add(self.filePaneFileOpsLabel1, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
		filePaneOperationsSizer.Add(self.sliderNumFileforChecking, 0, 0, 0)
		filePaneOperationsSizer.Add(self.filePaneFileOpsLabel2, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
		filePaneOperationsSizer.Add(self.buttonCheckItems, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		filePaneOperationsSizer.Add(self.fillerPanel1, 0, 0, 0)

		sizerControlItemsButtons = wx.GridSizer(2, 3, 0, 0)
		sizerControlItemsButtons.Add(self.expandAllTreeBranchesButton, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
		sizerControlItemsButtons.Add(self.expandCheckedItemsButton, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
		sizerControlItemsButtons.Add(self.checkAllItemsButton, 0, wx.EXPAND, 0)
		sizerControlItemsButtons.Add(self.collapseAllTreeBranchesButton, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
		sizerControlItemsButtons.Add(self.collapseCheckedItemsButton, 0, wx.EXPAND, 0)
		sizerControlItemsButtons.Add(self.uncheckAllItemsButton, 0, wx.EXPAND, 0)

		filePaneOperationsSizer.Add(sizerControlItemsButtons, 0, wx.EXPAND, 0)
		filePaneOperationsSizer.Add(self.fillerPanel2, 1, wx.EXPAND, 0)
		filePaneOperationsSizer.Add(self.buttonMoveFiles, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		notebookTreeSizer.Add(filePaneOperationsSizer, 0, wx.EXPAND, 0)
		self.notebookFilePane.SetSizer(notebookTreeSizer)
		configTabFilenameCleanerSizer.Add(self.configTabFilenameCleaningLabel, 0, wx.ALL, 3)
		configTabFilenameRECleanerGridSizer.Add(self.configTabREFilenameCleanerHeadingLabel, 0, 0, 0)
		configTabFilenameRECleanerGridSizer.Add(self.fillerPanel3, 1, wx.EXPAND, 0)
		configTabFilenameRECleanerGridSizer.Add(self.filenameCleanerRegexTextCtrl, 0, wx.EXPAND, 0)
		configTabFilenameRECleanerGridSizer.Add(self.regexValidLabel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
		configTabFilenameRECleanerGridSizer.Add(self.regexDocLabel, 0, 0, 0)
		configTabFilenameRECleanerGridSizer.Add(self.fillerPanel4, 1, wx.EXPAND, 0)
		configTabFilenameRECleanerGridSizer.AddGrowableCol(0)
		configTabFilenameCleanerSizer.Add(configTabFilenameRECleanerGridSizer, 0, wx.ALL|wx.EXPAND, 10)
		configTabFilenameCleanerGridSizer.Add(self.configTabFilenameCleanerHeadingStaticText, 0, 0, 0)
		configTabFilenameCleanerGridSizer.Add(self.fillerPanel3_copy, 1, wx.EXPAND, 0)
		configTabFilenameCleanerGridSizer.Add(self.filenameCleanerTextCtrl, 0, wx.EXPAND, 0)
		configTabFilenameCleanerGridSizer.Add(self.stripListValidLabel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
		configTabFilenameCleanerGridSizer.Add(self.stripListDocLabel, 0, 0, 0)
		configTabFilenameCleanerGridSizer.Add(self.fillerPanel4_copy, 1, wx.EXPAND, 0)
		configTabFilenameCleanerGridSizer.AddGrowableCol(0)
		configTabFilenameCleanerSizer.Add(configTabFilenameCleanerGridSizer, 0, wx.ALL|wx.EXPAND, 10)
		textStripEnclosingItemCheckboxesSizer.Add(self.configTabFilenameCleanerBracketRemvalStaticText, 0, 0, 0)
		textStripEnclosingItemCheckboxesSizer.Add(self.textCleanParenthesesCheckbox, 0, wx.LEFT|wx.RIGHT, 5)
		textStripEnclosingItemCheckboxesSizer.Add(self.textCleanBracketsCheckbox, 0, 0, 0)
		textStripEnclosingItemCheckboxesSizer.Add(self.textCleanCurlyBracketsCheckbox, 0, wx.LEFT|wx.RIGHT, 5)
		configTabFilenameCleanerSizer.Add(textStripEnclosingItemCheckboxesSizer, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
		configTabMainSizer.Add(configTabFilenameCleanerSizer, 0, wx.EXPAND, 0)
		configTabCompEngineSlidersSizer.Add(self.confingTabCompEngineLabel, 0, wx.ALL, 3)
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
		configTabCompEngineSlidersSizer.Add(specialOptionsGridSizer, 0, wx.ALL|wx.EXPAND, 10)
		configTabMainSizer.Add(configTabCompEngineSlidersSizer, 1, wx.EXPAND, 0)
		configTabMainSizer.Add(self.settingInstructions, 0, wx.ALL, 5)
		self.notebookConfigPane.SetSizer(configTabMainSizer)
		self.notebook.AddPage(self.notebookFilePane, "File List")
		self.notebook.AddPage(self.notebookConfigPane, "Settings")
		MainSizer.Add(self.notebook, 1, wx.EXPAND, 0)
		MainSizer.Add(self.statusWindow, 0, wx.EXPAND, 0)
		MainSizer.Add(self.StatusText, 0, wx.ALL, 5)
		self.SetSizer(MainSizer)
		MainSizer.Fit(self)
		self.Layout()


		redir=RedirectText(self.statusWindow)

		sys.stdout=redir
		#sys.sterr=redir

		self.treeRoot = self.fileTree.AddRoot("All")



		# end wxGlade

	def selectDirPressed(self, event): # wxGlade: MainFrame.<event_handler>

		self.openFolder.SetPath(self.fileSourceDir)
		if self.openFolder.ShowModal() == wx.ID_OK:
			self.startAddress.SetValue(self.openFolder.GetPath())

		event.Skip()

	def startDirProcessing(self, event): # wxGlade: MainFrame.<event_handler>

		#try:
		#	self.compar.close()
		#except:
		#	pass
		#the GC seems to catch and delete self.compar, unless sys.exit(0) is called

		self.fileSourceDir = self.startAddress.GetValue()
		self.config.stripTerms = self.filenameCleanerTextCtrl.Value.split(":")
		print "Stripping Terms: ", self.config.stripTerms


		if os.access(self.fileSourceDir, os.F_OK):
			print "Path OK"
			self.compar = comp.Comparator(self.config)
			self.compar.comp(self.fileSourceDir)

			self.trimmedDict = self.compar.trimTree(self.config.getCompThresh())
			print "Adding to Tree",
			#print self.trimmedDict
			if len(self.trimmedDict) < 1:
				print "No items. Either folder is empty or thresholds are set incorrectly."
			self.addDicttoTree(self.trimmedDict)
		else:
			print "Cannot Access Path %s" % self.fileSourceDir

		event.Skip()

	def checkItemsWithThreshold(self, event): # wxGlade: MainFrame.<event_handler>
		mainLevel = self.treeRoot.GetChildren()
		print mainLevel
		sliderVal = self.sliderNumFileforChecking.GetValue()
		for item in mainLevel:
			print item.GetText()
			childNum = len(item.GetChildren())
			if childNum >= sliderVal:
				item.Check()
				for child in item.GetChildren():
					child.Check()
			else:
				item.Check(False)
				for child in item.GetChildren():
					child.Check(False)
			print "has %s children" % childNum
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
		self.openFolder.SetPath(self.fileSourceDir)
		if self.openFolder.ShowModal() == wx.ID_OK:
			targetDir = self.openFolder.GetPath()

		print targetDir
		mainLevel = self.treeRoot.GetChildren()

		if self.fileSourceDir != None and mainLevel != [None]:
			for item in self.treeRoot.GetChildren():
				if item.IsChecked():
					currWorkingDir = os.path.join(targetDir, item.GetText())
					if not os.access(currWorkingDir, os.F_OK):
						print os.mkdir(currWorkingDir)
					for child in item.GetChildren():
						if child.IsChecked():
							fileName = child.GetData().fn
							originalFullPath = os.path.join(self.fileSourceDir, fileName)
							destFullPath = os.path.join(currWorkingDir, fileName)
							print "	", originalFullPath,
							if os.access(originalFullPath, os.F_OK):
								print shutil.move(originalFullPath, destFullPath)

			wx.GetApp().Yield(True)	#Yield execution to the GUI to allow printing


		print "Done moving Files"
		event.Skip()

	def checkPreprocessingRE(self, event): # wxGlade: MainFrame.<event_handler>
		print "Whoops - Regular expressions are not yet implemented"
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
			self.compar

			self.config.compThreshold = self.compThresholdSlider.GetValue()
			print "Recomputing similarity tree"
			print "Trimming Tree"
			self.trimmedDict = self.compar.trimTree(self.config.getCompThresh())
			#print "Adding Tree"
			#print self.trimmedDict
			self.addDicttoTree(self.trimmedDict)
		except:
			print "Need to run comparison first"


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
			if type(item) == str:
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

			for dict, simVal in group.items():
				tLen = len(dict.fn)
				if tLen > fnLen:
					fnLen = tLen
				tLen = len(dict.cn)
				if tLen > cnLen:
					cnLen = tLen
		for group in filesList:
			#print "Group"
			#print group.keys()[0].cn
			thisBranch = self.fileTree.AppendItem(self.treeRoot, group.keys()[0].cn.title(), ct_type=1)

			for dict, simVal in group.items():
				self.fileTree.AppendItem(thisBranch, "Cleaned String - : %s : - Original String - : %s  : - Similarity Metric Value: %s" % (dict.cn.ljust(cnLen+1), dict.fn.ljust(fnLen+1), simVal), ct_type=1, data=dict)
				#print self.fileTree.SetPyData(leafID, (dict, simVal))
				#print "	", dict.fn
			#print fnLen, cnLen
		try:
			self.treeRoot.Expand()
		except:
			pass

		print " - Done"

	def regenNotify(self, event):
		print "Note: you must rerun the file comparison to update results with new comparion coefficents"

	def handleExit(self, event):
		print "Exiting"
		try:
			self.compar.close()
		except:
			pass

		self.config.stripStr = self.filenameCleanerTextCtrl.Value
		#print self.config
		pickleOut = open("config.pik", "w")
		pickle.dump(self.config.dump(), pickleOut)
		#print self.config.dump()
		pickleOut.close

		sys.exit()
	# end of class MainFrame
