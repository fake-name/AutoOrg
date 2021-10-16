# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        if not MainWidget.objectName():
            MainWidget.setObjectName(u"MainWidget")
        MainWidget.resize(1000, 600)
        self.verticalLayout_2 = QVBoxLayout(MainWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.sliderNumFileforChecking_label = QTabWidget(MainWidget)
        self.sliderNumFileforChecking_label.setObjectName(u"sliderNumFileforChecking_label")
        self.sliderNumFileforChecking_label.setFocusPolicy(Qt.WheelFocus)
        self.view_tab = QWidget()
        self.view_tab.setObjectName(u"view_tab")
        self.verticalLayout = QVBoxLayout(self.view_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.sort_to_dir_label = QLabel(self.view_tab)
        self.sort_to_dir_label.setObjectName(u"sort_to_dir_label")

        self.gridLayout.addWidget(self.sort_to_dir_label, 1, 0, 1, 1)

        self.sort_into_dir = QLineEdit(self.view_tab)
        self.sort_into_dir.setObjectName(u"sort_into_dir")
        self.sort_into_dir.setReadOnly(False)

        self.gridLayout.addWidget(self.sort_into_dir, 1, 1, 1, 1)

        self.sort_source_location = QLineEdit(self.view_tab)
        self.sort_source_location.setObjectName(u"sort_source_location")

        self.gridLayout.addWidget(self.sort_source_location, 0, 1, 1, 1)

        self.target_directory_label = QLabel(self.view_tab)
        self.target_directory_label.setObjectName(u"target_directory_label")

        self.gridLayout.addWidget(self.target_directory_label, 0, 0, 1, 1)

        self.select_dir_button = QPushButton(self.view_tab)
        self.select_dir_button.setObjectName(u"select_dir_button")

        self.gridLayout.addWidget(self.select_dir_button, 0, 2, 1, 1)

        self.select_sort_into_dir_button = QPushButton(self.view_tab)
        self.select_sort_into_dir_button.setObjectName(u"select_sort_into_dir_button")

        self.gridLayout.addWidget(self.select_sort_into_dir_button, 1, 2, 1, 1)

        self.start_proc_button = QPushButton(self.view_tab)
        self.start_proc_button.setObjectName(u"start_proc_button")

        self.gridLayout.addWidget(self.start_proc_button, 0, 3, 1, 1)

        self.enable_disable_sort_to = QPushButton(self.view_tab)
        self.enable_disable_sort_to.setObjectName(u"enable_disable_sort_to")
        self.enable_disable_sort_to.setCheckable(True)
        self.enable_disable_sort_to.setChecked(True)

        self.gridLayout.addWidget(self.enable_disable_sort_to, 1, 3, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.treeView = QTreeView(self.view_tab)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout.addWidget(self.treeView)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.general_sim_slider_label = QLabel(self.view_tab)
        self.general_sim_slider_label.setObjectName(u"general_sim_slider_label")

        self.horizontalLayout_6.addWidget(self.general_sim_slider_label)

        self.comp_threshold_slider = QSlider(self.view_tab)
        self.comp_threshold_slider.setObjectName(u"comp_threshold_slider")
        self.comp_threshold_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_6.addWidget(self.comp_threshold_slider)

        self.com_threshold_slider_value_label = QLabel(self.view_tab)
        self.com_threshold_slider_value_label.setObjectName(u"com_threshold_slider_value_label")

        self.horizontalLayout_6.addWidget(self.com_threshold_slider_value_label)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.button_check_items = QPushButton(self.view_tab)
        self.button_check_items.setObjectName(u"button_check_items")

        self.horizontalLayout_7.addWidget(self.button_check_items)

        self.check_all_slder_sizer = QVBoxLayout()
        self.check_all_slder_sizer.setObjectName(u"check_all_slder_sizer")
        self.slider_num_file_for_checking = QSlider(self.view_tab)
        self.slider_num_file_for_checking.setObjectName(u"slider_num_file_for_checking")
        self.slider_num_file_for_checking.setMinimum(1)
        self.slider_num_file_for_checking.setMaximum(10)
        self.slider_num_file_for_checking.setOrientation(Qt.Horizontal)
        self.slider_num_file_for_checking.setTickPosition(QSlider.TicksAbove)
        self.slider_num_file_for_checking.setTickInterval(1)

        self.check_all_slder_sizer.addWidget(self.slider_num_file_for_checking)

        self.slider_num_file_for_checking_label = QLabel(self.view_tab)
        self.slider_num_file_for_checking_label.setObjectName(u"slider_num_file_for_checking_label")
        self.slider_num_file_for_checking_label.setAlignment(Qt.AlignCenter)

        self.check_all_slder_sizer.addWidget(self.slider_num_file_for_checking_label)


        self.horizontalLayout_7.addLayout(self.check_all_slder_sizer)

        self.file_pane_file_ops_label2 = QLabel(self.view_tab)
        self.file_pane_file_ops_label2.setObjectName(u"file_pane_file_ops_label2")

        self.horizontalLayout_7.addWidget(self.file_pane_file_ops_label2)

        self.expand_contract_buttons_sizer = QGridLayout()
        self.expand_contract_buttons_sizer.setObjectName(u"expand_contract_buttons_sizer")
        self.expand_tree = QPushButton(self.view_tab)
        self.expand_tree.setObjectName(u"expand_tree")

        self.expand_contract_buttons_sizer.addWidget(self.expand_tree, 0, 0, 1, 1)

        self.expand_checked_tree_items = QPushButton(self.view_tab)
        self.expand_checked_tree_items.setObjectName(u"expand_checked_tree_items")

        self.expand_contract_buttons_sizer.addWidget(self.expand_checked_tree_items, 0, 1, 1, 1)

        self.collapse_checked_tree_items = QPushButton(self.view_tab)
        self.collapse_checked_tree_items.setObjectName(u"collapse_checked_tree_items")

        self.expand_contract_buttons_sizer.addWidget(self.collapse_checked_tree_items, 1, 1, 1, 1)

        self.collapse_tree = QPushButton(self.view_tab)
        self.collapse_tree.setObjectName(u"collapse_tree")

        self.expand_contract_buttons_sizer.addWidget(self.collapse_tree, 1, 0, 1, 1)

        self.check_all_tree_items = QPushButton(self.view_tab)
        self.check_all_tree_items.setObjectName(u"check_all_tree_items")

        self.expand_contract_buttons_sizer.addWidget(self.check_all_tree_items, 0, 2, 1, 1)

        self.uncheck_all_tree_items = QPushButton(self.view_tab)
        self.uncheck_all_tree_items.setObjectName(u"uncheck_all_tree_items")

        self.expand_contract_buttons_sizer.addWidget(self.uncheck_all_tree_items, 1, 2, 1, 1)


        self.horizontalLayout_7.addLayout(self.expand_contract_buttons_sizer)

        self.button_move_files = QPushButton(self.view_tab)
        self.button_move_files.setObjectName(u"button_move_files")

        self.horizontalLayout_7.addWidget(self.button_move_files)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.sliderNumFileforChecking_label.addTab(self.view_tab, "")
        self.settings_tab = QWidget()
        self.settings_tab.setObjectName(u"settings_tab")
        self.verticalLayout_3 = QVBoxLayout(self.settings_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.settings_tab)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        self.verticalLayout_3.addWidget(self.label, 0, Qt.AlignTop)

        self.config_tab_filename_cleaner_heading_static_text = QLabel(self.settings_tab)
        self.config_tab_filename_cleaner_heading_static_text.setObjectName(u"config_tab_filename_cleaner_heading_static_text")

        self.verticalLayout_3.addWidget(self.config_tab_filename_cleaner_heading_static_text)

        self.lineEdit = QLineEdit(self.settings_tab)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_3.addWidget(self.lineEdit)

        self.strip_list_doc_label = QLabel(self.settings_tab)
        self.strip_list_doc_label.setObjectName(u"strip_list_doc_label")

        self.verticalLayout_3.addWidget(self.strip_list_doc_label)

        self.verticalSpacer_3 = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.settings_tab_strip_checkboxes_sizer = QHBoxLayout()
        self.settings_tab_strip_checkboxes_sizer.setObjectName(u"settings_tab_strip_checkboxes_sizer")
        self.settings_tab_strip_checkboxes_sizer.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.config_tab_filename_cleaner_bracket_remval_static_text = QLabel(self.settings_tab)
        self.config_tab_filename_cleaner_bracket_remval_static_text.setObjectName(u"config_tab_filename_cleaner_bracket_remval_static_text")

        self.settings_tab_strip_checkboxes_sizer.addWidget(self.config_tab_filename_cleaner_bracket_remval_static_text)

        self.text_clean_parentheses_checkbox = QCheckBox(self.settings_tab)
        self.text_clean_parentheses_checkbox.setObjectName(u"text_clean_parentheses_checkbox")

        self.settings_tab_strip_checkboxes_sizer.addWidget(self.text_clean_parentheses_checkbox)

        self.text_clean_brackets_checkbox = QCheckBox(self.settings_tab)
        self.text_clean_brackets_checkbox.setObjectName(u"text_clean_brackets_checkbox")

        self.settings_tab_strip_checkboxes_sizer.addWidget(self.text_clean_brackets_checkbox)

        self.text_clean_curly_brackets_checkbox = QCheckBox(self.settings_tab)
        self.text_clean_curly_brackets_checkbox.setObjectName(u"text_clean_curly_brackets_checkbox")

        self.settings_tab_strip_checkboxes_sizer.addWidget(self.text_clean_curly_brackets_checkbox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.settings_tab_strip_checkboxes_sizer.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.settings_tab_strip_checkboxes_sizer)

        self.verticalSpacer_2 = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.confing_tab_comp_engine_label = QLabel(self.settings_tab)
        self.confing_tab_comp_engine_label.setObjectName(u"confing_tab_comp_engine_label")
        self.confing_tab_comp_engine_label.setFont(font)

        self.verticalLayout_3.addWidget(self.confing_tab_comp_engine_label)

        self.label_word_length_weighting = QLabel(self.settings_tab)
        self.label_word_length_weighting.setObjectName(u"label_word_length_weighting")

        self.verticalLayout_3.addWidget(self.label_word_length_weighting)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.slider_word_length_weighting = QSlider(self.settings_tab)
        self.slider_word_length_weighting.setObjectName(u"slider_word_length_weighting")
        self.slider_word_length_weighting.setMinimum(1)
        self.slider_word_length_weighting.setMaximum(5000)
        self.slider_word_length_weighting.setValue(1000)
        self.slider_word_length_weighting.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.slider_word_length_weighting)

        self.value_word_length_weighting = QLabel(self.settings_tab)
        self.value_word_length_weighting.setObjectName(u"value_word_length_weighting")

        self.horizontalLayout_2.addWidget(self.value_word_length_weighting)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.label_str_length_difference_weighting = QLabel(self.settings_tab)
        self.label_str_length_difference_weighting.setObjectName(u"label_str_length_difference_weighting")

        self.verticalLayout_3.addWidget(self.label_str_length_difference_weighting)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.slider_str_length_difference_weighting = QSlider(self.settings_tab)
        self.slider_str_length_difference_weighting.setObjectName(u"slider_str_length_difference_weighting")
        self.slider_str_length_difference_weighting.setMinimum(1)
        self.slider_str_length_difference_weighting.setMaximum(5000)
        self.slider_str_length_difference_weighting.setValue(1000)
        self.slider_str_length_difference_weighting.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.slider_str_length_difference_weighting)

        self.value_str_length_difference_weighting = QLabel(self.settings_tab)
        self.value_str_length_difference_weighting.setObjectName(u"value_str_length_difference_weighting")

        self.horizontalLayout_3.addWidget(self.value_str_length_difference_weighting)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.label_word_length_difference_weighting = QLabel(self.settings_tab)
        self.label_word_length_difference_weighting.setObjectName(u"label_word_length_difference_weighting")

        self.verticalLayout_3.addWidget(self.label_word_length_difference_weighting)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.slider_word_length_difference_weighting = QSlider(self.settings_tab)
        self.slider_word_length_difference_weighting.setObjectName(u"slider_word_length_difference_weighting")
        self.slider_word_length_difference_weighting.setMinimum(1)
        self.slider_word_length_difference_weighting.setMaximum(5000)
        self.slider_word_length_difference_weighting.setValue(1000)
        self.slider_word_length_difference_weighting.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.slider_word_length_difference_weighting)

        self.value_word_length_difference_weighting = QLabel(self.settings_tab)
        self.value_word_length_difference_weighting.setObjectName(u"value_word_length_difference_weighting")

        self.horizontalLayout_4.addWidget(self.value_word_length_difference_weighting)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.setting_instructions = QLabel(self.settings_tab)
        self.setting_instructions.setObjectName(u"setting_instructions")

        self.verticalLayout_3.addWidget(self.setting_instructions)

        self.sliderNumFileforChecking_label.addTab(self.settings_tab, "")

        self.verticalLayout_2.addWidget(self.sliderNumFileforChecking_label)


        self.retranslateUi(MainWidget)

        self.sliderNumFileforChecking_label.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWidget)
    # setupUi

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QCoreApplication.translate("MainWidget", u"Form", None))
        self.sort_to_dir_label.setText(QCoreApplication.translate("MainWidget", u"Sort into directory:", None))
        self.target_directory_label.setText(QCoreApplication.translate("MainWidget", u"Directory to Process:", None))
        self.select_dir_button.setText(QCoreApplication.translate("MainWidget", u"Select Directory", None))
        self.select_sort_into_dir_button.setText(QCoreApplication.translate("MainWidget", u"Select Directory", None))
        self.start_proc_button.setText(QCoreApplication.translate("MainWidget", u"Run Sort", None))
        self.enable_disable_sort_to.setText(QCoreApplication.translate("MainWidget", u"Enable", None))
        self.general_sim_slider_label.setText(QCoreApplication.translate("MainWidget", u"Similarity Grouping Threshold", None))
        self.com_threshold_slider_value_label.setText(QCoreApplication.translate("MainWidget", u"1.000", None))
        self.button_check_items.setText(QCoreApplication.translate("MainWidget", u"Check all items with at least", None))
        self.slider_num_file_for_checking_label.setText(QCoreApplication.translate("MainWidget", u"2", None))
        self.file_pane_file_ops_label2.setText(QCoreApplication.translate("MainWidget", u"items in group.", None))
        self.expand_tree.setText(QCoreApplication.translate("MainWidget", u"Expand Tree", None))
        self.expand_checked_tree_items.setText(QCoreApplication.translate("MainWidget", u"Expand Checked", None))
        self.collapse_checked_tree_items.setText(QCoreApplication.translate("MainWidget", u"Collapse Checked", None))
        self.collapse_tree.setText(QCoreApplication.translate("MainWidget", u"Collapse Tree", None))
        self.check_all_tree_items.setText(QCoreApplication.translate("MainWidget", u"Check All", None))
        self.uncheck_all_tree_items.setText(QCoreApplication.translate("MainWidget", u"Uncheck All", None))
        self.button_move_files.setText(QCoreApplication.translate("MainWidget", u"Move selected files into Directory (Opens Folder Picker)", None))
        self.sliderNumFileforChecking_label.setTabText(self.sliderNumFileforChecking_label.indexOf(self.view_tab), QCoreApplication.translate("MainWidget", u"Sort", None))
        self.label.setText(QCoreApplication.translate("MainWidget", u"Pre-Comparison Filename Processing", None))
        self.config_tab_filename_cleaner_heading_static_text.setText(QCoreApplication.translate("MainWidget", u"Text Strip List", None))
        self.strip_list_doc_label.setText(QCoreApplication.translate("MainWidget", u"Colon (:) separated list of terms to remove from filenames before comparing. Case insensitive.\n"
"Note: Be certain to not leave any spurious spaces, they may disrupt text removal.", None))
        self.config_tab_filename_cleaner_bracket_remval_static_text.setText(QCoreApplication.translate("MainWidget", u"Strip out text in:", None))
        self.text_clean_parentheses_checkbox.setText(QCoreApplication.translate("MainWidget", u"Parentheses - ()", None))
        self.text_clean_brackets_checkbox.setText(QCoreApplication.translate("MainWidget", u"Square Brackets - []", None))
        self.text_clean_curly_brackets_checkbox.setText(QCoreApplication.translate("MainWidget", u"Curly Braces - {}", None))
        self.confing_tab_comp_engine_label.setText(QCoreApplication.translate("MainWidget", u"Comparison Engine Variables", None))
        self.label_word_length_weighting.setText(QCoreApplication.translate("MainWidget", u"Word Length Weighting", None))
        self.value_word_length_weighting.setText(QCoreApplication.translate("MainWidget", u"1.000", None))
        self.label_str_length_difference_weighting.setText(QCoreApplication.translate("MainWidget", u"String Length Diffrerence Weighting", None))
        self.value_str_length_difference_weighting.setText(QCoreApplication.translate("MainWidget", u"1.000", None))
        self.label_word_length_difference_weighting.setText(QCoreApplication.translate("MainWidget", u"Word Length Difference Weighting", None))
        self.value_word_length_difference_weighting.setText(QCoreApplication.translate("MainWidget", u"1.000", None))
        self.setting_instructions.setText(QCoreApplication.translate("MainWidget", u"All settings except the Similarity Grouping Threshold require a new comparison to be run to incorporate value changes", None))
        self.sliderNumFileforChecking_label.setTabText(self.sliderNumFileforChecking_label.indexOf(self.settings_tab), QCoreApplication.translate("MainWidget", u"Settings", None))
    # retranslateUi

