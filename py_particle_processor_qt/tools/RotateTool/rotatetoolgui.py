# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rotatetoolgui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RotateToolGUI(object):
    def setupUi(self, RotateToolGUI):
        RotateToolGUI.setObjectName("RotateToolGUI")
        RotateToolGUI.resize(257, 125)
        self.centralwidget = QtWidgets.QWidget(RotateToolGUI)
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
        self.type_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.type_label.setObjectName("type_label")
        self.gridLayout.addWidget(self.type_label, 0, 0, 1, 1)
        self.value_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.value_label.setObjectName("value_label")
        self.gridLayout.addWidget(self.value_label, 1, 0, 1, 1)
        self.type_combo = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.type_combo.setObjectName("type_combo")
        self.type_combo.addItem("")
        self.gridLayout.addWidget(self.type_combo, 0, 1, 1, 1)
        self.value = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.value.setText("")
        self.value.setObjectName("value")
        self.gridLayout.addWidget(self.value, 1, 1, 1, 1)
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
        RotateToolGUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(RotateToolGUI)
        QtCore.QMetaObject.connectSlotsByName(RotateToolGUI)

    def retranslateUi(self, RotateToolGUI):
        _translate = QtCore.QCoreApplication.translate
        RotateToolGUI.setWindowTitle(_translate("RotateToolGUI", "Scale Tool"))
        self.label.setText(_translate("RotateToolGUI", "Rotate Tool"))
        self.type_label.setText(_translate("RotateToolGUI", "Type:"))
        self.value_label.setText(_translate("RotateToolGUI", "Value"))
        self.type_combo.setItemText(0, _translate("RotateToolGUI", "Degrees"))
        self.value.setPlaceholderText(_translate("RotateToolGUI", "1.0"))
        self.cancel_button.setText(_translate("RotateToolGUI", "Cancel"))
        self.apply_button.setText(_translate("RotateToolGUI", "Apply"))

