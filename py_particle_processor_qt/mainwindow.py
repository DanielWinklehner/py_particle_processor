# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
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
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.centralWidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.treeWidget = QtWidgets.QTreeWidget(self.layoutWidget)
        self.treeWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.treeWidget.setAlternatingRowColors(True)
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
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.properties_label = QtWidgets.QLabel(self.layoutWidget1)
        self.properties_label.setObjectName("properties_label")
        self.verticalLayout_2.addWidget(self.properties_label)
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
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout_2.addWidget(self.textEdit_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
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
        self.menu_File.setObjectName("menu_File")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.actionImport_New = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionImport_New.setIcon(icon)
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
        self.actionUnload_Selected = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("remove")
        self.actionUnload_Selected.setIcon(icon)
        self.actionUnload_Selected.setObjectName("actionUnload_Selected")
        self.actionProperties = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("applications-system")
        self.actionProperties.setIcon(icon)
        self.actionProperties.setObjectName("actionProperties")
        self.actionPlot = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("emblem-photos")
        self.actionPlot.setIcon(icon)
        self.actionPlot.setObjectName("actionPlot")
        self.actionAnalyze = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("applications-accessories")
        self.actionAnalyze.setIcon(icon)
        self.actionAnalyze.setObjectName("actionAnalyze")
        self.mainToolBar.addAction(self.actionImport_New)
        self.mainToolBar.addAction(self.actionImport_Add)
        self.mainToolBar.addAction(self.actionUnload_Selected)
        self.mainToolBar.addAction(self.actionProperties)
        self.mainToolBar.addAction(self.actionAnalyze)
        self.mainToolBar.addAction(self.actionPlot)
        self.mainToolBar.addAction(self.actionExport_For)
        self.mainToolBar.addAction(self.actionQuit)
        self.menu_File.addAction(self.actionImport_New)
        self.menu_File.addAction(self.actionImport_Add)
        self.menu_File.addAction(self.actionUnload_Selected)
        self.menu_File.addAction(self.actionExport_For)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menu_File.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyParticleProcessor"))
        self.label.setText(_translate("MainWindow", "Datasets"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Selected"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "ID"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "Name"))
        self.properties_label.setText(_translate("MainWindow", "Properties"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menu_File.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionImport_New.setText(_translate("MainWindow", "Import New..."))
        self.actionImport_New.setIconText(_translate("MainWindow", "New..."))
        self.actionImport_New.setToolTip(_translate("MainWindow", "New..."))
        self.actionImport_Add.setText(_translate("MainWindow", "Import Add..."))
        self.actionImport_Add.setIconText(_translate("MainWindow", "Add..."))
        self.actionImport_Add.setToolTip(_translate("MainWindow", "Add..."))
        self.actionExport_For.setText(_translate("MainWindow", "Export For..."))
        self.actionExport_For.setIconText(_translate("MainWindow", "Export..."))
        self.actionExport_For.setToolTip(_translate("MainWindow", "Export..."))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionUnload_Selected.setText(_translate("MainWindow", "Remove"))
        self.actionUnload_Selected.setToolTip(_translate("MainWindow", "Unload"))
        self.actionProperties.setText(_translate("MainWindow", "Properties"))
        self.actionProperties.setToolTip(_translate("MainWindow", "Properties"))
        self.actionPlot.setText(_translate("MainWindow", "Plot"))
        self.actionPlot.setToolTip(_translate("MainWindow", "Plot"))
        self.actionAnalyze.setText(_translate("MainWindow", "Analyze"))
        self.actionAnalyze.setToolTip(_translate("MainWindow", "Analyze"))

from pyqtgraph import PlotWidget
from pyqtgraph.opengl import GLViewWidget
