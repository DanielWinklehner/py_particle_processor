# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'orbittoolgui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OrbitToolGUI(object):
    def setupUi(self, OrbitToolGUI):
        OrbitToolGUI.setObjectName("OrbitToolGUI")
        OrbitToolGUI.resize(323, 183)
        self.centralwidget = QtWidgets.QWidget(OrbitToolGUI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 321, 183))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.step_1_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.step_1_label.setObjectName("step_1_label")
        self.gridLayout.addWidget(self.step_1_label, 0, 0, 1, 1)
        self.step_2_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.step_2_label.setObjectName("step_2_label")
        self.gridLayout.addWidget(self.step_2_label, 1, 0, 1, 1)
        self.step_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.step_2.setText("")
        self.step_2.setObjectName("step_2")
        self.gridLayout.addWidget(self.step_2, 1, 1, 1, 1)
        self.step_3_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.step_3_label.setObjectName("step_3_label")
        self.gridLayout.addWidget(self.step_3_label, 2, 0, 1, 1)
        self.step_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.step_3.setText("")
        self.step_3.setObjectName("step_3")
        self.gridLayout.addWidget(self.step_3, 2, 1, 1, 1)
        self.step_1 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.step_1.setText("")
        self.step_1.setObjectName("step_1")
        self.gridLayout.addWidget(self.step_1, 0, 1, 1, 1)
        self.center_orbit = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.center_orbit.sizePolicy().hasHeightForWidth())
        self.center_orbit.setSizePolicy(sizePolicy)
        self.center_orbit.setObjectName("center_orbit")
        self.gridLayout.addWidget(self.center_orbit, 3, 1, 1, 1)
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
        OrbitToolGUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(OrbitToolGUI)
        QtCore.QMetaObject.connectSlotsByName(OrbitToolGUI)

    def retranslateUi(self, OrbitToolGUI):
        _translate = QtCore.QCoreApplication.translate
        OrbitToolGUI.setWindowTitle(_translate("OrbitToolGUI", "Orbit Tool"))
        self.label.setText(_translate("OrbitToolGUI", "Orbit Tool"))
        self.step_1_label.setText(_translate("OrbitToolGUI", "First Step:"))
        self.step_2_label.setText(_translate("OrbitToolGUI", "Second Step:"))
        self.step_2.setPlaceholderText(_translate("OrbitToolGUI", "1"))
        self.step_3_label.setText(_translate("OrbitToolGUI", "Third Step:"))
        self.step_3.setPlaceholderText(_translate("OrbitToolGUI", "2"))
        self.step_1.setPlaceholderText(_translate("OrbitToolGUI", "0"))
        self.center_orbit.setText(_translate("OrbitToolGUI", "Center Orbit (for R and PR)"))
        self.cancel_button.setText(_translate("OrbitToolGUI", "Cancel"))
        self.apply_button.setText(_translate("OrbitToolGUI", "Apply"))

