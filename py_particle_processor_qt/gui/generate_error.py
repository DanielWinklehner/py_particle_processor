# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generate_error.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Generate_Error(object):
    def setupUi(self, Generate_Error):
        Generate_Error.setObjectName("Generate_Error")
        Generate_Error.resize(291, 153)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Generate_Error.sizePolicy().hasHeightForWidth())
        Generate_Error.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(Generate_Error)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 30, 291, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox, 0, QtCore.Qt.AlignHCenter)
        self.dataset_label = QtWidgets.QLabel(self.centralwidget)
        self.dataset_label.setGeometry(QtCore.QRect(50, -40, 201, 107))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataset_label.sizePolicy().hasHeightForWidth())
        self.dataset_label.setSizePolicy(sizePolicy)
        self.dataset_label.setAlignment(QtCore.Qt.AlignCenter)
        self.dataset_label.setObjectName("dataset_label")
        self.verticalLayoutWidget.raise_()
        self.dataset_label.raise_()
        self.label.raise_()
        Generate_Error.setCentralWidget(self.centralwidget)

        self.retranslateUi(Generate_Error)
        QtCore.QMetaObject.connectSlotsByName(Generate_Error)

    def retranslateUi(self, Generate_Error):
        _translate = QtCore.QCoreApplication.translate
        Generate_Error.setWindowTitle(_translate("Generate_Error", "Properties"))
        self.label.setText(_translate("Generate_Error", "Please fill out all fields available."))
        self.dataset_label.setText(_translate("Generate_Error", "Parameter(s) Not Entered!"))

