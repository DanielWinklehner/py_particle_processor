# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tools/TranslateTool/translatetoolgui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TranslateToolGUI(object):
    def setupUi(self, TranslateToolGUI):
        TranslateToolGUI.setObjectName("TranslateToolGUI")
        TranslateToolGUI.resize(189, 157)
        self.centralwidget = QtWidgets.QWidget(TranslateToolGUI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 186, 155))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.x_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.x_label.setObjectName("x_label")
        self.gridLayout.addWidget(self.x_label, 0, 0, 1, 1)
        self.y_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.y_label.setObjectName("y_label")
        self.gridLayout.addWidget(self.y_label, 1, 0, 1, 1)
        self.z_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.z_label.setObjectName("z_label")
        self.gridLayout.addWidget(self.z_label, 2, 0, 1, 1)
        self.y_trans = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.y_trans.setObjectName("y_trans")
        self.gridLayout.addWidget(self.y_trans, 1, 1, 1, 1)
        self.x_trans = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.x_trans.setClearButtonEnabled(False)
        self.x_trans.setObjectName("x_trans")
        self.gridLayout.addWidget(self.x_trans, 0, 1, 1, 1)
        self.z_trans = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.z_trans.setObjectName("z_trans")
        self.gridLayout.addWidget(self.z_trans, 2, 1, 1, 1)
        self.m1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.m1.setObjectName("m1")
        self.gridLayout.addWidget(self.m1, 0, 2, 1, 1)
        self.m2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.m2.setObjectName("m2")
        self.gridLayout.addWidget(self.m2, 1, 2, 1, 1)
        self.m3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.m3.setObjectName("m3")
        self.gridLayout.addWidget(self.m3, 2, 2, 1, 1)
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
        TranslateToolGUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(TranslateToolGUI)
        QtCore.QMetaObject.connectSlotsByName(TranslateToolGUI)

    def retranslateUi(self, TranslateToolGUI):
        _translate = QtCore.QCoreApplication.translate
        TranslateToolGUI.setWindowTitle(_translate("TranslateToolGUI", "Scale Tool"))
        self.label.setText(_translate("TranslateToolGUI", "Translate Tool"))
        self.x_label.setText(_translate("TranslateToolGUI", "X"))
        self.y_label.setText(_translate("TranslateToolGUI", "Y"))
        self.z_label.setText(_translate("TranslateToolGUI", "Z"))
        self.y_trans.setText(_translate("TranslateToolGUI", "0.0"))
        self.x_trans.setText(_translate("TranslateToolGUI", "0.0"))
        self.z_trans.setText(_translate("TranslateToolGUI", "0.0"))
        self.m1.setText(_translate("TranslateToolGUI", "m"))
        self.m2.setText(_translate("TranslateToolGUI", "m"))
        self.m3.setText(_translate("TranslateToolGUI", "m"))
        self.cancel_button.setText(_translate("TranslateToolGUI", "Cancel"))
        self.apply_button.setText(_translate("TranslateToolGUI", "Apply"))

