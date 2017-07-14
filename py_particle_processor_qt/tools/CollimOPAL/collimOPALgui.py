# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'collimOPALgui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CollimOPAL(object):
    def setupUi(self, CollimOPAL):
        CollimOPAL.setObjectName("CollimOPAL")
        CollimOPAL.resize(421, 303)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CollimOPAL.sizePolicy().hasHeightForWidth())
        CollimOPAL.setSizePolicy(sizePolicy)
        CollimOPAL.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(CollimOPAL)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 3, 401, 300))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 200))
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.gap = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.gap.setObjectName("gap")
        self.gridLayout.addWidget(self.gap, 2, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.w = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.w.setObjectName("w")
        self.gridLayout.addWidget(self.w, 4, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.step = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.step.setObjectName("step")
        self.gridLayout.addWidget(self.step, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.hl = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.hl.setObjectName("hl")
        self.gridLayout.addWidget(self.hl, 3, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_3.addWidget(self.textBrowser, 0, QtCore.Qt.AlignVCenter)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox, 0, QtCore.Qt.AlignRight)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem)
        CollimOPAL.setCentralWidget(self.centralwidget)

        self.retranslateUi(CollimOPAL)
        QtCore.QMetaObject.connectSlotsByName(CollimOPAL)

    def retranslateUi(self, CollimOPAL):
        _translate = QtCore.QCoreApplication.translate
        CollimOPAL.setWindowTitle(_translate("CollimOPAL", "Generating Collimator"))
        self.label.setText(_translate("CollimOPAL", "<html><head/><body><p>Generate collimator code for OPAL-cycl.</p><p>The collimator will be perpendicular to the average momentum at the given step.</p></body></html>"))
        self.label_6.setText(_translate("CollimOPAL", "Gap Half-width (mm):"))
        self.label_7.setText(_translate("CollimOPAL", "Collimator Width (mm):"))
        self.label_2.setText(_translate("CollimOPAL", "Step Number:"))
        self.label_8.setText(_translate("CollimOPAL", "Collimator Half-length (mm):"))
        self.textBrowser.setHtml(_translate("CollimOPAL", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Collim_1:CCOLLIMATOR, XSTART=_, YSTART=_, XEND=_, YEND=_, WIDTH=_;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Collim_2:CCOLLIMATOR, XSTART=_, YSTART=_, XEND=_, YEND=_, WIDTH=_;</p></body></html>"))

