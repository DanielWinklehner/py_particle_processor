# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generate_envelope.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Generate_Envelope(object):
    def setupUi(self, Generate_Envelope):
        Generate_Envelope.setObjectName("Generate_Envelope")
        Generate_Envelope.resize(488, 648)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Generate_Envelope.sizePolicy().hasHeightForWidth())
        Generate_Envelope.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(Generate_Envelope)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 599))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setMaximumSize(QtCore.QSize(500, 25))
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.tr_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.tr_label.setObjectName("tr_label")
        self.gridLayout.addWidget(self.tr_label, 1, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.tl_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.tl_label.setObjectName("tl_label")
        self.gridLayout.addWidget(self.tl_label, 0, 1, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.zr = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.zr.setObjectName("zr")
        self.gridLayout.addWidget(self.zr, 2, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.zpos = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.zpos.setMinimumSize(QtCore.QSize(142, 0))
        self.zpos.setMaximumSize(QtCore.QSize(176, 16777215))
        self.zpos.setObjectName("zpos")
        self.zpos.addItem("")
        self.zpos.addItem("")
        self.zpos.addItem("")
        self.zpos.addItem("")
        self.zpos.addItem("")
        self.zpos.addItem("")
        self.gridLayout.addWidget(self.zpos, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.ze = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.ze.setEnabled(False)
        self.ze.setObjectName("ze")
        self.gridLayout.addWidget(self.ze, 4, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 1, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.bl_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.bl_label.setObjectName("bl_label")
        self.gridLayout.addWidget(self.bl_label, 2, 1, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.zmom = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.zmom.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zmom.sizePolicy().hasHeightForWidth())
        self.zmom.setSizePolicy(sizePolicy)
        self.zmom.setMinimumSize(QtCore.QSize(142, 0))
        self.zmom.setMaximumSize(QtCore.QSize(176, 16777215))
        self.zmom.setObjectName("zmom")
        self.zmom.addItem("")
        self.zmom.addItem("")
        self.zmom.addItem("")
        self.zmom.addItem("")
        self.gridLayout.addWidget(self.zmom, 1, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.zpstddev = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.zpstddev.setEnabled(False)
        self.zpstddev.setMinimumSize(QtCore.QSize(100, 0))
        self.zpstddev.setMaximumSize(QtCore.QSize(134, 16777215))
        self.zpstddev.setObjectName("zpstddev")
        self.gridLayout_3.addWidget(self.zpstddev, 0, 1, 1, 1, QtCore.Qt.AlignRight)
        self.zmstddev = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.zmstddev.setEnabled(False)
        self.zmstddev.setMinimumSize(QtCore.QSize(100, 0))
        self.zmstddev.setMaximumSize(QtCore.QSize(134, 16777215))
        self.zmstddev.setObjectName("zmstddev")
        self.gridLayout_3.addWidget(self.zmstddev, 1, 1, 1, 1, QtCore.Qt.AlignRight)
        self.gridLayout.addLayout(self.gridLayout_3, 5, 2, 1, 1)
        self.gridLayout.setRowMinimumHeight(0, 20)
        self.verticalLayout_3.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem1)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.xydist = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.xydist.setMinimumSize(QtCore.QSize(142, 0))
        self.xydist.setMaximumSize(QtCore.QSize(176, 16777215))
        self.xydist.setObjectName("xydist")
        self.xydist.addItem("")
        self.xydist.addItem("")
        self.xydist.addItem("")
        self.xydist.addItem("")
        self.verticalLayout_2.addWidget(self.xydist, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.yrp = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.yrp.setObjectName("yrp")
        self.gridLayout_2.addWidget(self.yrp, 7, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.bl_label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.bl_label_6.setObjectName("bl_label_6")
        self.gridLayout_2.addWidget(self.bl_label_6, 2, 1, 1, 1, QtCore.Qt.AlignRight)
        self.bl_label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.bl_label_3.setObjectName("bl_label_3")
        self.gridLayout_2.addWidget(self.bl_label_3, 7, 1, 1, 1, QtCore.Qt.AlignRight)
        self.tl_label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.tl_label_2.setObjectName("tl_label_2")
        self.gridLayout_2.addWidget(self.tl_label_2, 0, 1, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.ye = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.ye.setObjectName("ye")
        self.gridLayout_2.addWidget(self.ye, 8, 2, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 6, 0, 2, 1)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 8, 1, 1, 1, QtCore.Qt.AlignRight)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 9, 1, 1, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.yr = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.yr.setEnabled(True)
        self.yr.setObjectName("yr")
        self.gridLayout_2.addWidget(self.yr, 6, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.bl_label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.bl_label_4.setObjectName("bl_label_4")
        self.gridLayout_2.addWidget(self.bl_label_4, 6, 1, 1, 1, QtCore.Qt.AlignRight)
        self.tr_label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.tr_label_2.setObjectName("tr_label_2")
        self.gridLayout_2.addWidget(self.tr_label_2, 5, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.xe = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.xe.setEnabled(True)
        self.xe.setObjectName("xe")
        self.gridLayout_2.addWidget(self.xe, 3, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.bl_label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.bl_label_5.setObjectName("bl_label_5")
        self.gridLayout_2.addWidget(self.bl_label_5, 1, 1, 1, 1, QtCore.Qt.AlignRight)
        self.xr = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.xr.setEnabled(True)
        self.xr.setObjectName("xr")
        self.gridLayout_2.addWidget(self.xr, 1, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 1, 1, 1, QtCore.Qt.AlignRight)
        self.xrp = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.xrp.setEnabled(True)
        self.xrp.setObjectName("xrp")
        self.gridLayout_2.addWidget(self.xrp, 2, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 4, 1, 1, 1, QtCore.Qt.AlignRight)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_11 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_12 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.xstddev = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.xstddev.setEnabled(False)
        self.xstddev.setMinimumSize(QtCore.QSize(100, 0))
        self.xstddev.setMaximumSize(QtCore.QSize(134, 16777215))
        self.xstddev.setObjectName("xstddev")
        self.gridLayout_4.addWidget(self.xstddev, 0, 1, 1, 1, QtCore.Qt.AlignRight)
        self.xpstddev = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.xpstddev.setEnabled(False)
        self.xpstddev.setMinimumSize(QtCore.QSize(100, 0))
        self.xpstddev.setMaximumSize(QtCore.QSize(134, 16777215))
        self.xpstddev.setObjectName("xpstddev")
        self.gridLayout_4.addWidget(self.xpstddev, 1, 1, 1, 1, QtCore.Qt.AlignRight)
        self.gridLayout_2.addLayout(self.gridLayout_4, 4, 2, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_13 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_13.setObjectName("label_13")
        self.gridLayout_5.addWidget(self.label_13, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_14 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_14.setObjectName("label_14")
        self.gridLayout_5.addWidget(self.label_14, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.ystddev = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.ystddev.setEnabled(False)
        self.ystddev.setMinimumSize(QtCore.QSize(100, 0))
        self.ystddev.setMaximumSize(QtCore.QSize(134, 16777215))
        self.ystddev.setObjectName("ystddev")
        self.gridLayout_5.addWidget(self.ystddev, 0, 1, 1, 1, QtCore.Qt.AlignRight)
        self.ypstddev = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.ypstddev.setEnabled(False)
        self.ypstddev.setMinimumSize(QtCore.QSize(100, 0))
        self.ypstddev.setMaximumSize(QtCore.QSize(134, 16777215))
        self.ypstddev.setObjectName("ypstddev")
        self.gridLayout_5.addWidget(self.ypstddev, 1, 1, 1, 1, QtCore.Qt.AlignRight)
        self.gridLayout_2.addLayout(self.gridLayout_5, 9, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        Generate_Envelope.setCentralWidget(self.centralwidget)

        self.retranslateUi(Generate_Envelope)
        QtCore.QMetaObject.connectSlotsByName(Generate_Envelope)

    def retranslateUi(self, Generate_Envelope):
        _translate = QtCore.QCoreApplication.translate
        Generate_Envelope.setWindowTitle(_translate("Generate_Envelope", "Generate Distribution: Enter Parameters"))
        self.label.setText(_translate("Generate_Envelope", "Longitudinal Distribution"))
        self.tr_label.setText(_translate("Generate_Envelope", "Momentum:"))
        self.tl_label.setText(_translate("Generate_Envelope", "Position:"))
        self.label_2.setText(_translate("Generate_Envelope", "Normalized Emittance (pi-mm-mrad):"))
        self.zpos.setItemText(0, _translate("Generate_Envelope", "Constant"))
        self.zpos.setItemText(1, _translate("Generate_Envelope", "Uniform along length"))
        self.zpos.setItemText(2, _translate("Generate_Envelope", "Uniform on ellipse"))
        self.zpos.setItemText(3, _translate("Generate_Envelope", "Gaussian on ellipse"))
        self.zpos.setItemText(4, _translate("Generate_Envelope", "Waterbag"))
        self.zpos.setItemText(5, _translate("Generate_Envelope", "Parabolic"))
        self.label_3.setText(_translate("Generate_Envelope", "Standard Deviation:"))
        self.bl_label.setText(_translate("Generate_Envelope", "Length/Envelope Radius (mm):"))
        self.zmom.setItemText(0, _translate("Generate_Envelope", "Constant"))
        self.zmom.setItemText(1, _translate("Generate_Envelope", "Uniform along length"))
        self.zmom.setItemText(2, _translate("Generate_Envelope", "Uniform on ellipse"))
        self.zmom.setItemText(3, _translate("Generate_Envelope", "Gaussian on ellipse"))
        self.label_8.setText(_translate("Generate_Envelope", "Position (mm):"))
        self.label_9.setText(_translate("Generate_Envelope", "Momentum (mrad):"))
        self.label_4.setText(_translate("Generate_Envelope", "Transverse Distribution"))
        self.xydist.setItemText(0, _translate("Generate_Envelope", "Uniform"))
        self.xydist.setItemText(1, _translate("Generate_Envelope", "Gaussian"))
        self.xydist.setItemText(2, _translate("Generate_Envelope", "Waterbag"))
        self.xydist.setItemText(3, _translate("Generate_Envelope", "Parabolic"))
        self.bl_label_6.setText(_translate("Generate_Envelope", "Envelope Angle (mrad):"))
        self.bl_label_3.setText(_translate("Generate_Envelope", "Envelope Angle (mrad):"))
        self.tl_label_2.setText(_translate("Generate_Envelope", "X Phase Space Ellipse:"))
        self.label_5.setText(_translate("Generate_Envelope", "Normalized Emittance (pi-mm-mrad):"))
        self.label_6.setText(_translate("Generate_Envelope", "Standard Deviation:"))
        self.bl_label_4.setText(_translate("Generate_Envelope", "Envelope Radius (mm):"))
        self.tr_label_2.setText(_translate("Generate_Envelope", "Y Phase Space Ellipse:"))
        self.bl_label_5.setText(_translate("Generate_Envelope", "Envelope Radius (mm):"))
        self.label_7.setText(_translate("Generate_Envelope", "Normalized Emittance (pi-mm-mrad):"))
        self.label_10.setText(_translate("Generate_Envelope", "Standard Deviation:"))
        self.label_11.setText(_translate("Generate_Envelope", "Radius (mm):"))
        self.label_12.setText(_translate("Generate_Envelope", "Angle (mrad):"))
        self.label_13.setText(_translate("Generate_Envelope", "Radius (mm):"))
        self.label_14.setText(_translate("Generate_Envelope", "Angle (mrad):"))

