from propertieswindow import Ui_PropertiesWindow
from PyQt5.QtWidgets import qApp, QFileDialog
from PyQt5 import QtGui, QtCore
import pyqtgraph as pg


class PropertyManager(object):
    def __init__(self, settings, debug=False):
        self._settings = settings
        self._debug = debug

        if self._debug:
            print("DEBUG: Initializing PropertyManager instance")

        self._propWindow= QtGui.QMainWindow()
        self._propWindowGUI = Ui_PropertiesWindow()
        self._propWindowGUI.setupUi(self._propWindow)

        if len(self._settings) > 0:
            self.populate_settings()
        else:
            self.retrieve_settings()

        self._propWindowGUI.apply_button.clicked.connect(self.apply_callback)
        self._propWindowGUI.cancel_button.clicked.connect(self.cancel_callback)

    def populate_settings(self):

        if self._debug:
            print("DEBUG: populate_settings called")

        # Top Left:
        self._propWindowGUI.tl_enabled.setCheckState(self._settings["tl_en"])
        self._propWindowGUI.tl_combo_a.setCurrentIndex(self._settings["tl_a"])
        self._propWindowGUI.tl_combo_b.setCurrentIndex(self._settings["tl_b"])

        # Top Right:
        self._propWindowGUI.tr_enabled.setCheckState(self._settings["tr_en"])
        self._propWindowGUI.tr_combo_a.setCurrentIndex(self._settings["tr_a"])
        self._propWindowGUI.tr_combo_b.setCurrentIndex(self._settings["tr_b"])

        # Bottom Left:
        self._propWindowGUI.bl_enabled.setCheckState(self._settings["bl_en"])
        self._propWindowGUI.bl_combo_a.setCurrentIndex(self._settings["bl_a"])
        self._propWindowGUI.bl_combo_b.setCurrentIndex(self._settings["bl_b"])

        # 3D Plot:
        self._propWindowGUI.three_d_enabled.setCheckState(self._settings["3d_en"])

    def retrieve_settings(self):

        if self._debug:
            print("DEBUG: retrieve_settings called")

        # Top Left:
        self._settings["tl_en"] = self._propWindowGUI.tl_enabled.checkState()
        self._settings["tl_a"] = self._propWindowGUI.tl_combo_a.currentIndex()
        self._settings["tl_b"] = self._propWindowGUI.tl_combo_b.currentIndex()

        # Top Right:
        self._settings["tr_en"] = self._propWindowGUI.tr_enabled.checkState()
        self._settings["tr_a"] = self._propWindowGUI.tr_combo_a.currentIndex()
        self._settings["tr_b"] = self._propWindowGUI.tr_combo_b.currentIndex()

        # Bottom Left:
        self._settings["bl_en"] = self._propWindowGUI.bl_enabled.checkState()
        self._settings["bl_a"] = self._propWindowGUI.bl_combo_a.currentIndex()
        self._settings["bl_b"] = self._propWindowGUI.bl_combo_b.currentIndex()

        # 3D Plot:
        self._settings["3d_en"] = self._propWindowGUI.three_d_enabled.checkState()

    def get_settings(self):
        return self._settings

    def apply_callback(self):

        if self._debug:
            print("DEBUG: apply_callback called")

        self.retrieve_settings()
        self._propWindow.close()

        if self._debug:
            print("DEBUG: Closing Plot Properties Window")

        return 0

    def cancel_callback(self):

        if self._debug:
            print("DEBUG: cancel_callback called")

        self._propWindow.close()

        if self._debug:
            print("DEBUG: Closing Plot Properties Window")

        return 0

    def run(self):

        if self._debug:
            print("DEBUG: Running PropertyManager")

        # --- Show the GUI --- #
        self._propWindow.show()

if __name__ == "__main__":
    app = QtGui.QApplication([])
    pm = PropertyManager(settings={}, debug=True)
    print(pm.run())
    app.exec_()