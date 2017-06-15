# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tools/ScaleTool/scaletoolgui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ScaleToolGUI(object):
    def setupUi(self, ScaleToolGUI):
        ScaleToolGUI.setObjectName("ScaleToolGUI")
        ScaleToolGUI.resize(257, 125)
        self.centralwidget = QtWidgets.QWidget(ScaleToolGUI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 254, 122))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.parameter_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.parameter_label.setObjectName("parameter_label")
        self.gridLayout.addWidget(self.parameter_label, 0, 0, 1, 1)
        self.scaling_factor_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.scaling_factor_label.setObjectName("scaling_factor_label")
        self.gridLayout.addWidget(self.scaling_factor_label, 1, 0, 1, 1)
        self.parameter_combo = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.parameter_combo.setObjectName("parameter_combo")
        self.parameter_combo.addItem("")
        self.parameter_combo.addItem("")
        self.parameter_combo.addItem("")
        self.parameter_combo.addItem("")
        self.parameter_combo.addItem("")
        self.parameter_combo.addItem("")
        self.parameter_combo.addItem("")
        self.parameter_combo.addItem("")
        self.parameter_combo.addItem("")
        self.parameter_combo.addItem("")
        self.gridLayout.addWidget(self.parameter_combo, 0, 1, 1, 1)
        self.scaling_factor = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.scaling_factor.setText("")
        self.scaling_factor.setObjectName("scaling_factor")
        self.gridLayout.addWidget(self.scaling_factor, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.apply_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.apply_button.setDefault(True)
        self.apply_button.setObjectName("apply_button")
        self.horizontalLayout.addWidget(self.apply_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        ScaleToolGUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(ScaleToolGUI)
        QtCore.QMetaObject.connectSlotsByName(ScaleToolGUI)

    def retranslateUi(self, ScaleToolGUI):
        _translate = QtCore.QCoreApplication.translate
        ScaleToolGUI.setWindowTitle(_translate("ScaleToolGUI", "Scale Tool"))
        self.label.setText(_translate("ScaleToolGUI", "Scale Tool"))
        self.parameter_label.setText(_translate("ScaleToolGUI", "Parameter(s):"))
        self.scaling_factor_label.setText(_translate("ScaleToolGUI", "Scaling Factor:"))
        self.parameter_combo.setItemText(0, _translate("ScaleToolGUI", "X, Y, Z"))
        self.parameter_combo.setItemText(1, _translate("ScaleToolGUI", "X, Y"))
        self.parameter_combo.setItemText(2, _translate("ScaleToolGUI", "X"))
        self.parameter_combo.setItemText(3, _translate("ScaleToolGUI", "Y"))
        self.parameter_combo.setItemText(4, _translate("ScaleToolGUI", "Z"))
        self.parameter_combo.setItemText(5, _translate("ScaleToolGUI", "PX, PY, PZ"))
        self.parameter_combo.setItemText(6, _translate("ScaleToolGUI", "PX, PY"))
        self.parameter_combo.setItemText(7, _translate("ScaleToolGUI", "PX"))
        self.parameter_combo.setItemText(8, _translate("ScaleToolGUI", "PY"))
        self.parameter_combo.setItemText(9, _translate("ScaleToolGUI", "PZ"))
        self.scaling_factor.setPlaceholderText(_translate("ScaleToolGUI", "1.0"))
        self.cancel_button.setText(_translate("ScaleToolGUI", "Cancel"))
        self.apply_button.setText(_translate("ScaleToolGUI", "Apply"))

