from ..abstract_tool import AbstractTool
from PyQt5.QtWidgets import QMainWindow
from .collimOPALgui import Ui_CollimOPAL
import numpy as np
import string


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
        self._datasource = None  # h5py datasource for orbit data

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
        self._settings["label"] = int(self._collimOPALGUI.num.text())
        self._settings["nseg"] = int(self._collimOPALGUI.nseg.text())

    def callback_apply(self):

        self.apply_settings()

        script = ""
        script += self.gen_script()

        self._collimOPALGUI.textBrowser.setText(script)

    # @staticmethod
    # def read_data(fn):
    #
    #     with open(fn, 'r') as infile:
    #         lines = infile.readlines()
    #
    #     design_particle_lines = []
    #
    #     for line in lines:
    #         if "ID0" in line:
    #             design_particle_lines.append(line.strip())
    #
    #     npts = len(design_particle_lines)
    #
    #     x = np.zeros(npts)
    #     y = np.zeros(npts)
    #     px = np.zeros(npts)
    #     py = np.zeros(npts)
    #
    #     for i, line in enumerate(design_particle_lines):
    #         _, _x, _px, _y, _py, _, _ = line.split()
    #         x[i] = float(_x) * 1000.0
    #         y[i] = float(_y) * 1000.0
    #         px[i] = float(_px)
    #         py[i] = float(_py)
    #
    #     return np.array([x, px, y, py])

    def gen_script(self):
        script = ""
        letters = list(string.ascii_lowercase)

        # Central collimator placement
        x_cent = np.mean(np.array(self._datasource["Step#{}".format(self._settings["step"])]["x"]))
        y_cent = np.mean(np.array(self._datasource["Step#{}".format(self._settings["step"])]["y"]))

        for n in range(self._settings["nseg"]):
            i = self._settings["step"]

            if n != 0:  # n = 0 indicates the central segment
                x_temp = np.mean(np.array(self._datasource["Step#{}".format(i)]["x"]))
                y_temp = np.mean(np.array(self._datasource["Step#{}".format(i)]["y"]))
                if n % 2 == 1:  # n congruent to 1 mod 2 indicates placement ahead of the central segment
                    while np.sqrt(np.square(x_cent - x_temp) + np.square(y_cent - y_temp)) \
                            < (int(n / 2) + (n % 2 > 0)) * self._settings["cwidth"]:
                        i += 1
                        x_temp = np.mean(np.array(self._datasource["Step#{}".format(i)]["x"]))
                        y_temp = np.mean(np.array(self._datasource["Step#{}".format(i)]["y"]))
                else:  # n > 0 congruent to 0 mod 2 indicates placement behind of the central segment
                    while np.sqrt(np.square(x_cent - x_temp) + np.square(y_cent - y_temp)) \
                            < (int(n / 2) + (n % 2 > 0)) * self._settings["cwidth"]:
                        i -= 1
                        x_temp = np.mean(np.array(self._datasource["Step#{}".format(i)]["x"]))
                        y_temp = np.mean(np.array(self._datasource["Step#{}".format(i)]["y"]))

            x_new = np.mean(np.array(self._datasource["Step#{}".format(i)]["x"]))
            y_new = np.mean(np.array(self._datasource["Step#{}".format(i)]["y"]))
            px_new = np.mean(np.array(self._datasource["Step#{}".format(i)]["px"]))
            py_new = np.mean(np.array(self._datasource["Step#{}".format(i)]["py"]))

            collim = self.gen_collim(x_new, y_new, px_new, py_new)

            script += "Collim_{}{}:CCOLLIMATOR, XSTART={}, YSTART={}, XEND={}, YEND={}, WIDTH={};\n\n" \
                .format(self._settings["label"], letters[2 * n], collim["x1a"], collim["y1a"], collim["x1b"],
                        collim["y1b"], self._settings["cwidth"])
            script += "Collim_{}{}:CCOLLIMATOR, XSTART={}, YSTART={}, XEND={}, YEND={}, WIDTH={};\n\n" \
                .format(self._settings["label"], letters[2 * n + 1], collim["x2a"], collim["y2a"], collim["x2b"],
                        collim["y2b"], self._settings["cwidth"])
        return script

    def gen_collim(self, x, y, px, py):
        # Find angle to rotate collimator according to momentum
        theta = np.arccos(px/np.sqrt(np.square(px) + np.square(py)))
        if py < 0:
            theta = -theta
        theta1 = theta + np.pi/2
        theta2 = theta - np.pi/2

        # Calculate coordinates
        x1a = self._settings["width"]*np.cos(theta1) + x
        x2a = self._settings["width"]*np.cos(theta2) + x
        x1b = (self._settings["width"] + self._settings["length"])*np.cos(theta1) + x
        x2b = (self._settings["width"] + self._settings["length"])*np.cos(theta2) + x

        y1a = self._settings["width"]*np.sin(theta1) + y
        y2a = self._settings["width"]*np.sin(theta2) + y
        y1b = (self._settings["width"] + self._settings["length"])*np.sin(theta1) + y
        y2b = (self._settings["width"] + self._settings["length"])*np.sin(theta2) + y

        return {"x1a": x1a, "x2a": x2a, "x1b": x1b, "x2b": x2b, "y1a": y1a, "y2a": y2a, "y1b": y1b, "y2b": y2b}

    # @staticmethod
    # def read(filename):
    #     text_file = open("C:/Users/Maria/PycharmProjects/py_particle_processor"
    #                      "/py_particle_processor_qt/tools/CollimOPAL/{}.txt".format(filename), "r")
    #     lines = text_file.read().split(',')
    #     data = np.array(lines).astype(np.float)
    #     text_file.close()
    #     return data

    def run(self):
        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._collimOPALWindow.width())
        _y = 0.5 * (screen_size.height() - self._collimOPALWindow.height())

        # --- Show the GUI --- #
        self._collimOPALWindow.show()
        self._collimOPALWindow.move(_x, _y)

    def open_gui(self):

        # Get parent dataset/source for orbit data
        dataset = self._selections[0]
        self._datasource = dataset.get_datasource()

        self.run()
