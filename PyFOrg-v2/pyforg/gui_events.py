# This Python file uses the following encoding: utf-8
import shutil
import traceback
import pickle
import os
import json
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QTreeWidgetItem
from PySide2.QtWidgets import QTreeWidget
from PySide2.QtCore import Qt

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

		self.gui.slider_num_file_for_checking           .valueChanged.connect(self.handler_check_slider_changed)

		self.gui.text_clean_parentheses_checkbox   .stateChanged.connect(self.handler_update_checkboxes_config_evt)
		self.gui.text_clean_brackets_checkbox      .stateChanged.connect(self.handler_update_checkboxes_config_evt)
		self.gui.text_clean_curly_brackets_checkbox.stateChanged.connect(self.handler_update_checkboxes_config_evt)


		self.gui.expand_tree                  .clicked.connect(self.handler_expand_tree)
		self.gui.expand_checked_tree_items    .clicked.connect(self.handler_expand_checked_tree_items)
		self.gui.check_all_tree_items         .clicked.connect(self.handler_check_all_tree_items)
		self.gui.collapse_checked_tree_items  .clicked.connect(self.handler_collapse_checked_tree_items)
		self.gui.collapse_tree                .clicked.connect(self.handler_collapse_tree)
		self.gui.uncheck_all_tree_items       .clicked.connect(self.handler_uncheck_all_tree_items)
		self.gui.collapse_unchecked_tree_items.clicked.connect(self.handler_collapse_unchecked_tree_items)
		self.gui.expand_unchecked_tree_items  .clicked.connect(self.handler_expand_unchecked_tree_items)

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

		if not self.config.enable_sort_to_dir:
			self.gui.sort_into_dir.setEnabled(False)
			self.gui.select_sort_into_dir_button.setEnabled(False)
			self.gui.enable_disable_sort_to.setText("Enable")
		else:
			self.gui.sort_into_dir.setEnabled(True)
			self.gui.select_sort_into_dir_button.setEnabled(True)
			self.gui.enable_disable_sort_to.setText("Disable")

	def handler_word_length_weighting_adjusted(self, _event):
		self.config.word_length_weighting = float(self.gui.slider_word_length_weighting.value())
		textVal = self.config.word_length_weighting / 1000
		self.gui.value_word_length_weighting.setText("%0.3f" % textVal)


	def handler_str_len_difference_adjusted(self, _event):
		self.config.str_length_weighting = float(self.gui.slider_str_length_difference_weighting.value())
		textVal = self.config.str_length_weighting / 1000
		self.gui.value_str_length_difference_weighting.setText("%0.3f" % textVal)

	def handler_word_len_difference_weighting_adjusted(self, _event):
		self.config.word_difference_weighting = float(self.gui.slider_word_length_difference_weighting.value())
		textVal = self.config.word_difference_weighting / 1000
		self.gui.value_word_length_difference_weighting.setText("%0.3f" % textVal)

	def handler_threshold_slider_adjusted(self, _event):
		self.config.comp_threshold = self.gui.comp_threshold_slider.value()
		self.gui.com_threshold_slider_value_label.setText("%0.3f" % self.config.getCompThresh())

	def handler_check_slider_changed(self, _event):
		val = self.gui.slider_num_file_for_checking.value()
		self.gui.slider_num_file_for_checking_label.setText("%s" % val)

	def handler_update_checkboxes_config_evt(self, _event):
		self.config.parentheses  = self.gui.text_clean_parentheses_checkbox   .isChecked()
		self.config.brackets     = self.gui.text_clean_brackets_checkbox      .isChecked()
		self.config.curly_braces = self.gui.text_clean_curly_brackets_checkbox.isChecked()

	def handler_threshold_slider_changed(self):
		try:
			assert self.compar
			print("Recomputing similarity tree")
			print("Trimming Tree")
			trimmed_dict = self.compar.trimTree(self.config.getCompThresh())
			#print "Adding Tree"
			#print trimmed_dict
			self.add_dict_to_tree(trimmed_dict)
		except:
			traceback.print_stack()
			print("Need to run comparison first")


	def closeEvent(self, _event):
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

	def handler_start_dir_processing(self, _event):

		self.config.strip_str   = self.gui.filename_cleaner_text_ctrl.text()
		self.config.sort_from_dir  = self.gui.sort_source_location.text()
		self.config.sort_to_dir = self.gui.sort_into_dir.text()

		terms = self.gui.filename_cleaner_text_ctrl.text().split(":")
		terms = [tmp for tmp in terms if tmp]
		self.config.strip_terms = terms

		if self.config.enable_sort_to_dir and not os.access(self.config.sort_to_dir, os.F_OK):
			msg_box = QMessageBox()
			msg_box.setText("Cannot Access Path %s" % self.config.sort_to_dir)
			msg_box.exec_()
			return

		if not os.access(self.config.sort_from_dir, os.F_OK):
			msg_box = QMessageBox()
			msg_box.setText("Cannot Access Path %s" % self.config.sort_from_dir)
			msg_box.exec_()
			return


		self.compar = file_comparator.Comparator(self.config)

		if self.config.enable_sort_to_dir:
			self.compar.sort_into(self.config.sort_from_dir, self.config.sort_to_dir)
		else:
			self.compar.sort(self.config.sort_from_dir)

		trimmed_dict = self.compar.trimTree(self.config.getCompThresh())

		#print trimmed_dict
		if len(trimmed_dict) < 1:
			print("No items. Either folder is empty or thresholds are set incorrectly.")
		self.add_dict_to_tree(trimmed_dict)


	def add_dict_to_tree(self, filesList):
		self.gui.file_tree.clear()

		for group in filesList:
			parent = QTreeWidgetItem(self.gui.file_tree)

			parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

			source_item = None
			for item_object, simVal in group.items():

				if simVal == "Source":
					parent.setText(0, "{}".format(item_object.fn))
					parent.setText(3, "{}".format(item_object.src_fqpath))
					source_item = item_object

			assert source_item is not None
			for item_object, simVal in group.items():

				if simVal == "Source":
					continue


				branch = QTreeWidgetItem(parent)
				branch.setFlags(branch.flags() | Qt.ItemIsUserCheckable)

				branch.setText(0, item_object.cn)
				branch.setText(1, item_object.fn)
				branch.setText(2, "%s" % (item_object.src_fqpath, ))
				branch.setText(3, "%s" % (item_object.dest_fqpath, ))
				if isinstance(simVal, (int, float)):
					branch.setText(4, "%0.5f" % (simVal, ))
				else:
					branch.setText(4, "%s" % (simVal, ))
				branch.setCheckState(0, Qt.Unchecked)
				branch.item_data = item_object



		self.gui.file_tree.setColumnWidth(0, 400)
		self.gui.file_tree.setColumnWidth(1, 400)
		self.gui.file_tree.setColumnWidth(2, 100)
		self.gui.file_tree.setColumnWidth(3, 100)
		self.gui.file_tree.setColumnWidth(4, 100)


	def handler_check_items_with_threshold(self, _event):
		slider_val = self.gui.slider_num_file_for_checking.value()

		for idx in range(self.gui.file_tree.topLevelItemCount()):
			item = self.gui.file_tree.topLevelItem(idx)

			child_cnt = item.childCount()

			if child_cnt >= slider_val:
				item.setCheckState(0, Qt.Checked)
			else:
				item.setCheckState(0, Qt.Unchecked)


	def handler_expand_tree(self, _event):
		self.gui.file_tree.expandAll()

	def handler_collapse_tree(self, _event):
		self.gui.file_tree.collapseAll()

	def handler_check_all_tree_items(self, _event):
		for idx in range(self.gui.file_tree.topLevelItemCount()):
			item = self.gui.file_tree.topLevelItem(idx)
			item.setCheckState(0, Qt.Checked)


	def handler_uncheck_all_tree_items(self, _event):
		for idx in range(self.gui.file_tree.topLevelItemCount()):
			item = self.gui.file_tree.topLevelItem(idx)
			item.setCheckState(0, Qt.Unchecked)

	def handler_collapse_checked_tree_items(self, _event):

		for idx in range(self.gui.file_tree.topLevelItemCount()):
			item = self.gui.file_tree.topLevelItem(idx)
			checked = item.checkState(0)

			if checked in [Qt.Checked, Qt.PartiallyChecked]:
				item.setExpanded(False)

	def handler_expand_checked_tree_items(self, _event):
		for idx in range(self.gui.file_tree.topLevelItemCount()):
			item = self.gui.file_tree.topLevelItem(idx)
			checked = item.checkState(0)

			if checked in [Qt.Checked, Qt.PartiallyChecked]:
				item.setExpanded(True)

	def handler_collapse_unchecked_tree_items(self, _event):

		for idx in range(self.gui.file_tree.topLevelItemCount()):
			item = self.gui.file_tree.topLevelItem(idx)
			checked = item.checkState(0)

			if checked == Qt.Unchecked:
				item.setExpanded(False)

	def handler_expand_unchecked_tree_items(self, _event):
		for idx in range(self.gui.file_tree.topLevelItemCount()):
			item = self.gui.file_tree.topLevelItem(idx)
			checked = item.checkState(0)

			if checked == Qt.Unchecked:
				item.setExpanded(True)

	# ----------------------------------------------
	# To Update


	def handler_move_selected_items_into_new_folders(self, _event):
		file_source_dir = self.gui.sort_source_location.text()

		if self.config.enable_sort_to_dir:
			output_folder = self.config.sort_to_dir
		else:
			output_folder = QFileDialog.getExistingDirectory(self,
				caption = 'Select directory to create new folders in'
				)

		if not output_folder:
			return


		for root_idx in range(self.gui.file_tree.topLevelItemCount()):
			item = self.gui.file_tree.topLevelItem(root_idx)

			child_cnt = item.childCount()
			checked = item.checkState(0)

			if checked in [Qt.Checked, Qt.PartiallyChecked]:
				# Column 0 is the header column
				dir_name = item.text(0)
				item_folder_name = os.path.join(output_folder, dir_name)
				print("Item output dir: '%s'" % (item_folder_name, ))
				if not os.access(item_folder_name, os.F_OK):
					print("need to make dir")
					# os.mkdir(item_folder_name)

				for child_idx in range(child_cnt):
					child = item.child(child_idx)
					child_checked = child.checkState(0)
					if child_checked == Qt.Checked:
						item_fn = child.item_data.fn
						source_fn = os.path.join(file_source_dir, item_fn)
						dest_fn = os.path.join(item_folder_name, item_fn)
						print("Should move from '%s' to '%s'" % (source_fn, dest_fn))
						if os.access(dest_fn, os.F_OK):
							print("destination file already exists!")
						elif os.access(source_fn, os.F_OK):
							print("Move would be OK?")
						else:
							print("what? Cannot access source?")
							# shutil.move(originalFullPath, destFullPath)
