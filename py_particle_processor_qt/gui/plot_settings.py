# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/plot_settings.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PlotSettingsWindow(object):
    def setupUi(self, PlotSettingsWindow):
        PlotSettingsWindow.setObjectName("PlotSettingsWindow")
        PlotSettingsWindow.resize(317, 186)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PlotSettingsWindow.sizePolicy().hasHeightForWidth())
        PlotSettingsWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(PlotSettingsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 317, 183))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_label.sizePolicy().hasHeightForWidth())
        self.main_label.setSizePolicy(sizePolicy)
        self.main_label.setObjectName("main_label")
        self.verticalLayout_3.addWidget(self.main_label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.three_d_enabled = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.three_d_enabled.setFocusPolicy(QtCore.Qt.NoFocus)
        self.three_d_enabled.setCheckable(True)
        self.three_d_enabled.setObjectName("three_d_enabled")
        self.gridLayout.addWidget(self.three_d_enabled, 1, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.three_d_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.three_d_label.setObjectName("three_d_label")
        self.gridLayout.addWidget(self.three_d_label, 1, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.step_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.step_label.setObjectName("step_label")
        self.gridLayout.addWidget(self.step_label, 0, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.step_input = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.step_input.sizePolicy().hasHeightForWidth())
        self.step_input.setSizePolicy(sizePolicy)
        self.step_input.setMinimum(0)
        self.step_input.setMaximum(999999999)
        self.step_input.setObjectName("step_input")
        self.gridLayout.addWidget(self.step_input, 0, 1, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.param_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.param_label.setObjectName("param_label")
        self.gridLayout.addWidget(self.param_label, 2, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.param_combo_a = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.param_combo_a.setObjectName("param_combo_a")
        self.param_combo_a.addItem("")
        self.param_combo_a.addItem("")
        self.param_combo_a.addItem("")
        self.param_combo_a.addItem("")
        self.param_combo_a.addItem("")
        self.param_combo_a.addItem("")
        self.horizontalLayout.addWidget(self.param_combo_a)
        self.param_combo_c = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.param_combo_c.setObjectName("param_combo_c")
        self.param_combo_c.addItem("")
        self.param_combo_c.addItem("")
        self.param_combo_c.addItem("")
        self.param_combo_c.addItem("")
        self.param_combo_c.addItem("")
        self.param_combo_c.addItem("")
        self.horizontalLayout.addWidget(self.param_combo_c)
        self.param_combo_b = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.param_combo_b.setEnabled(False)
        self.param_combo_b.setObjectName("param_combo_b")
        self.param_combo_b.addItem("")
        self.param_combo_b.addItem("")
        self.param_combo_b.addItem("")
        self.param_combo_b.addItem("")
        self.param_combo_b.addItem("")
        self.param_combo_b.addItem("")
        self.horizontalLayout.addWidget(self.param_combo_b)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.redraw_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.redraw_label.setObjectName("redraw_label")
        self.gridLayout.addWidget(self.redraw_label, 3, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.redraw_enabled = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.redraw_enabled.setChecked(True)
        self.redraw_enabled.setObjectName("redraw_enabled")
        self.gridLayout.addWidget(self.redraw_enabled, 3, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.verticalLayout_3.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.redraw_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.redraw_button.setObjectName("redraw_button")
        self.horizontalLayout_9.addWidget(self.redraw_button)
        spacerItem2 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.cancel_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_9.addWidget(self.cancel_button)
        self.apply_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.apply_button.setDefault(True)
        self.apply_button.setObjectName("apply_button")
        self.horizontalLayout_9.addWidget(self.apply_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        PlotSettingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PlotSettingsWindow)
        self.param_combo_c.setCurrentIndex(1)
        self.param_combo_b.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(PlotSettingsWindow)

    def retranslateUi(self, PlotSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        PlotSettingsWindow.setWindowTitle(_translate("PlotSettingsWindow", "Properties"))
        self.main_label.setText(_translate("PlotSettingsWindow", "PLOT SETTINGS"))
        self.three_d_enabled.setText(_translate("PlotSettingsWindow", "Enabled"))
        self.three_d_label.setText(_translate("PlotSettingsWindow", "3D"))
        self.step_label.setText(_translate("PlotSettingsWindow", "Step #:"))
        self.param_label.setText(_translate("PlotSettingsWindow", "Parameters"))
        self.param_combo_a.setItemText(0, _translate("PlotSettingsWindow", "X"))
        self.param_combo_a.setItemText(1, _translate("PlotSettingsWindow", "Y"))
        self.param_combo_a.setItemText(2, _translate("PlotSettingsWindow", "Z"))
        self.param_combo_a.setItemText(3, _translate("PlotSettingsWindow", "PX"))
        self.param_combo_a.setItemText(4, _translate("PlotSettingsWindow", "PY"))
        self.param_combo_a.setItemText(5, _translate("PlotSettingsWindow", "PZ"))
        self.param_combo_c.setItemText(0, _translate("PlotSettingsWindow", "X"))
        self.param_combo_c.setItemText(1, _translate("PlotSettingsWindow", "Y"))
        self.param_combo_c.setItemText(2, _translate("PlotSettingsWindow", "Z"))
        self.param_combo_c.setItemText(3, _translate("PlotSettingsWindow", "PX"))
        self.param_combo_c.setItemText(4, _translate("PlotSettingsWindow", "PY"))
        self.param_combo_c.setItemText(5, _translate("PlotSettingsWindow", "PZ"))
        self.param_combo_b.setItemText(0, _translate("PlotSettingsWindow", "X"))
        self.param_combo_b.setItemText(1, _translate("PlotSettingsWindow", "Y"))
        self.param_combo_b.setItemText(2, _translate("PlotSettingsWindow", "Z"))
        self.param_combo_b.setItemText(3, _translate("PlotSettingsWindow", "PX"))
        self.param_combo_b.setItemText(4, _translate("PlotSettingsWindow", "PY"))
        self.param_combo_b.setItemText(5, _translate("PlotSettingsWindow", "PZ"))
        self.redraw_label.setText(_translate("PlotSettingsWindow", "Redraw On Selection: "))
        self.redraw_enabled.setText(_translate("PlotSettingsWindow", "Enabled"))
        self.redraw_button.setText(_translate("PlotSettingsWindow", "Redraw"))
        self.cancel_button.setText(_translate("PlotSettingsWindow", "Cancel"))
        self.apply_button.setText(_translate("PlotSettingsWindow", "Apply"))
