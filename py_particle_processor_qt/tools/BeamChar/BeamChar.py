from ..abstract_tool import AbstractTool
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from .beamchargui import Ui_BeamChar
from matplotlib.ticker import LinearLocator
import matplotlib.pyplot as plt
import numpy as np


""""
A tool for plotting beam characteristics.
"""


class BeamChar(AbstractTool):
    def __init__(self, parent):
        super(BeamChar, self).__init__(parent)
        self._name = "Beam Characteristics"
        self._parent = parent
        self._filename = ""
        self._settings = {}

        # --- Initialize the GUI --- #
        self._beamCharWindow = QMainWindow()
        self._beamCharGUI = Ui_BeamChar()
        self._beamCharGUI.setupUi(self._beamCharWindow)

        self._beamCharGUI.buttonBox.accepted.connect(self.callback_apply)
        self._beamCharGUI.buttonBox.rejected.connect(self._beamCharWindow.close)

        self._has_gui = True
        self._need_selection = True
        self._min_selections = 1
        self._max_selections = 1
        self._redraw_on_exit = False

    def apply_settings(self):
        self._settings["rms"] = self._beamCharGUI.rms.isChecked()

        self._settings["halo"] = self._beamCharGUI.halo.isChecked()

    def callback_apply(self):
        self.apply_settings()
        self._beamCharWindow.close()
        self._parent.send_status("Creating plot(s)...")
        
        for dataset in self._selections:

            corrected = {}
            plot_data = {"xRMS": np.array([]), "yRMS": np.array([]), "zRMS": np.array([]),
                         "xHalo": np.array([]), "yHalo": np.array([]), "zHalo": np.array([])}

            datasource = dataset.get_datasource()

            nsteps, npart = dataset.get_nsteps(), dataset.get_npart()

            for step in range(nsteps):
                corrected["Step#{}".format(step)] = {}

                x_val = np.array(datasource["Step#{}".format(step)]["x"])
                y_val = np.array(datasource["Step#{}".format(step)]["y"])
                z_val = np.array(datasource["Step#{}".format(step)]["z"])

                # Center the beam
                corrected["Step#{}".format(step)]["x"] = x_val - np.mean(x_val)
                corrected["Step#{}".format(step)]["y"] = y_val - np.mean(y_val)
                corrected["Step#{}".format(step)]["z"] = z_val - np.mean(z_val)

                # Calculate RMS, if necessary
                if self._settings["rms"]:
                    plot_data["xRMS"] = np.append(plot_data["xRMS"], self.rms(x_val))
                    plot_data["yRMS"] = np.append(plot_data["yRMS"], self.rms(y_val))
                    plot_data["zRMS"] = np.append(plot_data["zRMS"], self.rms(z_val))

                # Calculate halo parameter, if necessary
                if self._settings["halo"]:
                    plot_data["xHalo"] = np.append(plot_data["xHalo"], self.halo(x_val))
                    plot_data["yHalo"] = np.append(plot_data["yHalo"], self.halo(y_val))
                    plot_data["zHalo"] = np.append(plot_data["zHalo"], self.halo(z_val))

        # Save plots as separate images, with appropriate titles
        if self._settings["rms"]:
            fig = plt.figure()
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            plt.rc('text', usetex=True)
            plt.rc('grid', linestyle=':')

            ax1 = plt.subplot(311)
            plt.title("RMS Beam Size (m)")
            plt.plot(range(nsteps), plot_data["xRMS"], 'k', lw=0.8)
            ax1.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            plt.grid()
            plt.ylabel("x")

            ax2 = plt.subplot(312, sharex=ax1)
            plt.plot(range(nsteps), plot_data["yRMS"], 'k', lw=0.8)
            ax2.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            plt.grid()
            plt.ylabel("y")

            ax3 = plt.subplot(313, sharex=ax1)
            plt.plot(range(nsteps), plot_data["zRMS"], 'k', lw=0.8)
            ax3.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            plt.grid()
            plt.xlabel("Turn")
            plt.ylabel("z")
            fig.tight_layout()
            fig.savefig(self._filename[0] + '_rmsBeamSize.png', dpi=600)

        if self._settings["halo"]:
            fig = plt.figure()
            ax = plt.axes()
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            plt.rc('text', usetex=True)

            ax1 = plt.subplot(311)
            plt.title("Halo Parameter")
            plt.plot(range(nsteps), plot_data["xHalo"], 'k', lw=0.8)
            ax1.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            plt.grid()
            plt.ylabel("x")

            ax2 = plt.subplot(312, sharex=ax1)
            plt.plot(range(nsteps), plot_data["yHalo"], 'k', lw=0.8)
            ax2.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            plt.grid()
            plt.ylabel("y")

            ax3 = plt.subplot(313, sharex=ax1)
            plt.plot(range(nsteps), plot_data["zHalo"], 'k', lw=0.8)
            ax3.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            plt.grid()
            plt.xlabel("Turn")
            plt.ylabel("z")
            fig.tight_layout()
            fig.savefig(self._filename[0] + '_haloParameter.png', bbox_inches='tight', dpi=600)

        self._parent.send_status("Plot(s) saved successfully!")

    @staticmethod
    def rms(nparray):
        mean_sqrd = np.mean(np.square(nparray))
        return np.sqrt(mean_sqrd)

    @staticmethod
    def halo(nparray):
        mean_sqrd = np.mean(np.square(nparray))
        mean_frth = np.mean(np.square(np.square(nparray)))
        return mean_frth/(np.square(mean_sqrd)) - 1.0

    def run(self):
        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._beamCharWindow.width())
        _y = 0.5 * (screen_size.height() - self._beamCharWindow.height())

        # --- Show the GUI --- #
        self._beamCharWindow.show()
        self._beamCharWindow.move(_x, _y)

    def open_gui(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        self._filename = QFileDialog.getSaveFileName(caption="Saving plots...", options=options,
                                                    filter="Image (*.png)")

        self.run()
