# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(994, 654)
        MainWindow.setStyleSheet("background-color: rgb(65, 65, 65);\n"
"alternate-background-color: rgb(130, 130, 130);\n"
"color: rgb(255, 255, 255);")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 2, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.splitter.setFrameShape(QtWidgets.QFrame.Box)
        self.splitter.setFrameShadow(QtWidgets.QFrame.Plain)
        self.splitter.setLineWidth(0)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(6)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.datasets_label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.datasets_label.sizePolicy().hasHeightForWidth())
        self.datasets_label.setSizePolicy(sizePolicy)
        self.datasets_label.setObjectName("datasets_label")
        self.verticalLayout.addWidget(self.datasets_label, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.treeWidget = QtWidgets.QTreeWidget(self.layoutWidget)
        self.treeWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.treeWidget.setAlternatingRowColors(False)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.treeWidget.setTextElideMode(QtCore.Qt.ElideRight)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setDefaultSectionSize(80)
        self.treeWidget.header().setMinimumSectionSize(1)
        self.treeWidget.header().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.treeWidget)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.properties_label = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.properties_label.sizePolicy().hasHeightForWidth())
        self.properties_label.setSizePolicy(sizePolicy)
        self.properties_label.setObjectName("properties_label")
        self.horizontalLayout_3.addWidget(self.properties_label)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.properties_combo = QtWidgets.QComboBox(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.properties_combo.sizePolicy().hasHeightForWidth())
        self.properties_combo.setSizePolicy(sizePolicy)
        self.properties_combo.setObjectName("properties_combo")
        self.horizontalLayout_3.addWidget(self.properties_combo)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)
        self.properties_table = QtWidgets.QTableWidget(self.layoutWidget1)
        self.properties_table.setRowCount(1)
        self.properties_table.setColumnCount(2)
        self.properties_table.setObjectName("properties_table")
        self.properties_table.horizontalHeader().setStretchLastSection(True)
        self.properties_table.verticalHeader().setVisible(False)
        self.properties_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.properties_table)
        self.tabWidget = QtWidgets.QTabWidget(self.splitter_2)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.tab.setObjectName("tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(7)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.graphicsView_1 = PlotWidget(self.tab)
        self.graphicsView_1.setObjectName("graphicsView_1")
        self.gridLayout_3.addWidget(self.graphicsView_1, 0, 0, 1, 1)
        self.graphicsView_2 = PlotWidget(self.tab)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.gridLayout_3.addWidget(self.graphicsView_2, 0, 1, 1, 1)
        self.graphicsView_3 = PlotWidget(self.tab)
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.gridLayout_3.addWidget(self.graphicsView_3, 1, 0, 1, 1)
        self.graphicsView_4 = GLViewWidget(self.tab)
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.gridLayout_3.addWidget(self.graphicsView_4, 1, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainToolBar.sizePolicy().hasHeightForWidth())
        self.mainToolBar.setSizePolicy(sizePolicy)
        self.mainToolBar.setIconSize(QtCore.QSize(16, 16))
        self.mainToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 994, 25))
        self.menuBar.setDefaultUp(True)
        self.menuBar.setNativeMenuBar(True)
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtWidgets.QMenu(self.menuBar)
        self.menu_File.setFocusPolicy(QtCore.Qt.NoFocus)
        self.menu_File.setObjectName("menu_File")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        self.menuPlot = QtWidgets.QMenu(self.menuBar)
        self.menuPlot.setObjectName("menuPlot")
        MainWindow.setMenuBar(self.menuBar)
        self.actionImport_New = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionImport_New.setIcon(icon)
        self.actionImport_New.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.actionImport_New.setPriority(QtWidgets.QAction.NormalPriority)
        self.actionImport_New.setObjectName("actionImport_New")
        self.actionImport_Add = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("add")
        self.actionImport_Add.setIcon(icon)
        self.actionImport_Add.setObjectName("actionImport_Add")
        self.actionExport_For = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("go-right")
        self.actionExport_For.setIcon(icon)
        self.actionExport_For.setObjectName("actionExport_For")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("exit")
        self.actionQuit.setIcon(icon)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionRemove = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("remove")
        self.actionRemove.setIcon(icon)
        self.actionRemove.setObjectName("actionRemove")
        self.actionAnalyze = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("applications-accessories")
        self.actionAnalyze.setIcon(icon)
        self.actionAnalyze.setObjectName("actionAnalyze")
        self.actionNew_Plot = QtWidgets.QAction(MainWindow)
        self.actionNew_Plot.setObjectName("actionNew_Plot")
        self.actionModify_Plot = QtWidgets.QAction(MainWindow)
        self.actionModify_Plot.setObjectName("actionModify_Plot")
        self.actionRemove_Plot = QtWidgets.QAction(MainWindow)
        self.actionRemove_Plot.setObjectName("actionRemove_Plot")
        self.actionRedraw = QtWidgets.QAction(MainWindow)
        self.actionRedraw.setObjectName("actionRedraw")
        self.actionGenerate = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("emblem-photos")
        self.actionGenerate.setIcon(icon)
        self.actionGenerate.setObjectName("actionGenerate")
        self.mainToolBar.addAction(self.actionImport_New)
        self.mainToolBar.addAction(self.actionImport_Add)
        self.mainToolBar.addAction(self.actionRemove)
        self.mainToolBar.addAction(self.actionGenerate)
        self.mainToolBar.addAction(self.actionAnalyze)
        self.mainToolBar.addAction(self.actionExport_For)
        self.mainToolBar.addAction(self.actionQuit)
        self.menu_File.addAction(self.actionImport_New)
        self.menu_File.addAction(self.actionImport_Add)
        self.menu_File.addAction(self.actionRemove)
        self.menu_File.addAction(self.actionExport_For)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuPlot.addAction(self.actionRedraw)
        self.menuPlot.addSeparator()
        self.menuPlot.addAction(self.actionNew_Plot)
        self.menuPlot.addAction(self.actionModify_Plot)
        self.menuPlot.addAction(self.actionRemove_Plot)
        self.menuBar.addAction(self.menu_File.menuAction())
        self.menuBar.addAction(self.menuPlot.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyParticleProcessor"))
        self.datasets_label.setText(_translate("MainWindow", "Datasets"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Selected"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "ID"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "Name"))
        self.properties_label.setText(_translate("MainWindow", "Properties:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Default Plots"))
        self.menu_File.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuPlot.setTitle(_translate("MainWindow", "Plot"))
        self.actionImport_New.setText(_translate("MainWindow", "Import New..."))
        self.actionImport_New.setIconText(_translate("MainWindow", "New..."))
        self.actionImport_New.setToolTip(_translate("MainWindow", "New..."))
        self.actionImport_Add.setText(_translate("MainWindow", "Import Add..."))
        self.actionImport_Add.setIconText(_translate("MainWindow", "Add..."))
        self.actionImport_Add.setToolTip(_translate("MainWindow", "Add..."))
        self.actionExport_For.setText(_translate("MainWindow", "Export..."))
        self.actionExport_For.setIconText(_translate("MainWindow", "Export..."))
        self.actionExport_For.setToolTip(_translate("MainWindow", "Export..."))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionRemove.setText(_translate("MainWindow", "Remove"))
        self.actionRemove.setToolTip(_translate("MainWindow", "Remove"))
        self.actionAnalyze.setText(_translate("MainWindow", "Analyze"))
        self.actionAnalyze.setToolTip(_translate("MainWindow", "Analyze"))
        self.actionNew_Plot.setText(_translate("MainWindow", "New Plot..."))
        self.actionModify_Plot.setText(_translate("MainWindow", "Modify Current Plot..."))
        self.actionRemove_Plot.setText(_translate("MainWindow", "Remove Current Plot"))
        self.actionRedraw.setText(_translate("MainWindow", "Redraw"))
        self.actionGenerate.setText(_translate("MainWindow", "Generate..."))
        self.actionGenerate.setIconText(_translate("MainWindow", "Generate..."))
        self.actionGenerate.setToolTip(_translate("MainWindow", "Generate distribution"))

from pyqtgraph import PlotWidget
from pyqtgraph.opengl import GLViewWidget
