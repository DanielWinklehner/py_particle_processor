from ..abstract_tool import AbstractTool
from PyQt5.QtWidgets import QMainWindow
from .collimOPALgui import Ui_CollimOPAL
import numpy as np


""""
A tool for generating collimator code for OPAL.
"""


class CollimOPAL(AbstractTool):
    def __init__(self, parent):
        super(CollimOPAL, self).__init__(parent)
        self._name = "Generate Collimator"
        self._parent = parent
        self._filename = ""
        self._settings = {}

        # --- Initialize the GUI --- #
        self._collimOPALWindow = QMainWindow()
        self._collimOPALGUI = Ui_CollimOPAL()
        self._collimOPALGUI.setupUi(self._collimOPALWindow)

        self._collimOPALGUI.buttonBox.accepted.connect(self.callback_apply)
        self._collimOPALGUI.buttonBox.rejected.connect(self._collimOPALWindow.close)

        self._has_gui = True
        self._need_selection = True
        self._min_selections = 1
        self._max_selections = 1
        self._redraw_on_exit = False

    def apply_settings(self):
        self._settings["step"] = int(self._collimOPALGUI.step.text())
        self._settings["width"] = float(self._collimOPALGUI.gap.text())
        self._settings["length"] = float(self._collimOPALGUI.hl.text())
        self._settings["cwidth"] = float(self._collimOPALGUI.w.text())

    def callback_apply(self):
        self.apply_settings()
        datasource = self._selections[0].get_datasource()

        x_avg = 1000.0 * np.mean(np.array(datasource["Step#{}".format(self._settings["step"])]["x"]))
        y_avg = 1000.0 * np.mean(np.array(datasource["Step#{}".format(self._settings["step"])]["y"]))
        px_avg = np.mean(np.array(datasource["Step#{}".format(self._settings["step"])]["px"]))
        py_avg = np.mean(np.array(datasource["Step#{}".format(self._settings["step"])]["py"]))

        # Find angle to rotate collimator according to momentum
        theta1 = np.arccos(px_avg/np.sqrt(np.square(px_avg) + np.square(py_avg)))
        theta2 = np.arccos(px_avg/np.sqrt(np.square(px_avg) + np.square(py_avg))) + np.pi

        x1a = self._settings["width"]*np.cos(theta1) + x_avg
        x2a = self._settings["width"]*np.cos(theta2) + x_avg
        x1b = (self._settings["width"] + self._settings["length"])*np.cos(theta1) + x_avg
        x2b = (self._settings["width"] + self._settings["length"])*np.cos(theta2) + x_avg

        y1a = self._settings["width"]*np.sin(theta1) + y_avg
        y2a = self._settings["width"]*np.sin(theta2) + y_avg
        y1b = (self._settings["width"] + self._settings["length"])*np.sin(theta1) + y_avg
        y2b = (self._settings["width"] + self._settings["length"])*np.sin(theta2) + y_avg

        script = "Collim_1:CCOLLIMATOR, XSTART={}, YSTART={}, XEND={}, YEND={}, WIDTH={};\n\n"\
            .format(x1a, y1a, x1b, y1b, self._settings["cwidth"])
        script += "Collim_2:CCOLLIMATOR, XSTART={}, YSTART={}, XEND={}, YEND={}, WIDTH={};"\
            .format(x2a, y2a, x2b, y2b, self._settings["cwidth"])

        self._collimOPALGUI.textBrowser.setText(script)


    def run(self):
        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._collimOPALWindow.width())
        _y = 0.5 * (screen_size.height() - self._collimOPALWindow.height())

        # --- Show the GUI --- #
        self._collimOPALWindow.show()
        self._collimOPALWindow.move(_x, _y)

    def open_gui(self):

        self.run()
