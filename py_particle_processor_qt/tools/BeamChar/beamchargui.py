# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beamchargui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BeamChar(object):
    def setupUi(self, BeamChar):
        BeamChar.setObjectName("BeamChar")
        BeamChar.resize(421, 303)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BeamChar.sizePolicy().hasHeightForWidth())
        BeamChar.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(BeamChar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 3, 401, 299))
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
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 1)
        self.intens = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.intens.setText("")
        self.intens.setObjectName("intens")
        self.gridLayout.addWidget(self.intens, 10, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.centroid = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.centroid.setText("")
        self.centroid.setObjectName("centroid")
        self.gridLayout.addWidget(self.centroid, 6, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.rms = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.rms.setText("")
        self.rms.setObjectName("rms")
        self.gridLayout.addWidget(self.rms, 2, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.halo = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.halo.setText("")
        self.halo.setObjectName("halo")
        self.gridLayout.addWidget(self.halo, 4, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 9, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.turnsep = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.turnsep.setText("")
        self.turnsep.setObjectName("turnsep")
        self.gridLayout.addWidget(self.turnsep, 5, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.ehist = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ehist.setText("")
        self.ehist.setObjectName("ehist")
        self.gridLayout.addWidget(self.ehist, 9, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 10, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 8, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.xz = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.xz.setText("")
        self.xz.setObjectName("xz")
        self.gridLayout.addWidget(self.xz, 8, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        BeamChar.setCentralWidget(self.centralwidget)

        self.retranslateUi(BeamChar)
        QtCore.QMetaObject.connectSlotsByName(BeamChar)

    def retranslateUi(self, BeamChar):
        _translate = QtCore.QCoreApplication.translate
        BeamChar.setWindowTitle(_translate("BeamChar", "Choosing Plots"))
        self.label.setText(_translate("BeamChar", "<html><head/><body><p>Please select the beam characteristic(s) you would like to plot.</p></body></html>"))
        self.label_9.setText(_translate("BeamChar", "Probes & Collimators"))
        self.label_8.setText(_translate("BeamChar", "Full Simulation"))
        self.label_4.setText(_translate("BeamChar", "Centroid Position"))
        self.label_3.setText(_translate("BeamChar", "Halo Parameter"))
        self.label_2.setText(_translate("BeamChar", "RMS Beam Size"))
        self.label_6.setText(_translate("BeamChar", "Energy Histogram"))
        self.label_5.setText(_translate("BeamChar", "Turn Separation"))
        self.label_7.setText(_translate("BeamChar", "Beam Intensity vs Radius"))
        self.label_10.setText(_translate("BeamChar", "X-Z Density Plot"))
