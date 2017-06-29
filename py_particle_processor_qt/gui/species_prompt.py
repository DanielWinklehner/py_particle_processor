# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/species_prompt.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SpeciesPrompt(object):
    def setupUi(self, SpeciesPrompt):
        SpeciesPrompt.setObjectName("SpeciesPrompt")
        SpeciesPrompt.resize(324, 70)
        SpeciesPrompt.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.centralwidget = QtWidgets.QWidget(SpeciesPrompt)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 321, 68))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.species_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.species_label.setObjectName("species_label")
        self.horizontalLayout.addWidget(self.species_label)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.species_selection = QtWidgets.QComboBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.species_selection.sizePolicy().hasHeightForWidth())
        self.species_selection.setSizePolicy(sizePolicy)
        self.species_selection.setObjectName("species_selection")
        self.horizontalLayout.addWidget(self.species_selection)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem1 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.apply_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.apply_button.setDefault(True)
        self.apply_button.setObjectName("apply_button")
        self.horizontalLayout_9.addWidget(self.apply_button)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        SpeciesPrompt.setCentralWidget(self.centralwidget)

        self.retranslateUi(SpeciesPrompt)
        QtCore.QMetaObject.connectSlotsByName(SpeciesPrompt)

    def retranslateUi(self, SpeciesPrompt):
        _translate = QtCore.QCoreApplication.translate
        SpeciesPrompt.setWindowTitle(_translate("SpeciesPrompt", "Species Prompt"))
        self.species_label.setText(_translate("SpeciesPrompt", "Ion Species:"))
        self.apply_button.setText(_translate("SpeciesPrompt", "Apply"))

