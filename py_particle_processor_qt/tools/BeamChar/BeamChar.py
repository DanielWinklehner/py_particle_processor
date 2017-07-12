from ..abstract_tool import AbstractTool
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from .beamchargui import Ui_BeamChar
from matplotlib.ticker import LinearLocator, FuncFormatter
from matplotlib.ticker import FormatStrFormatter
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
        self._max_selections = None
        self._redraw_on_exit = False

    def apply_settings(self):
        self._settings["rms"] = self._beamCharGUI.rms.isChecked()
        self._settings["halo"] = self._beamCharGUI.halo.isChecked()
        self._settings["centroid"] = self._beamCharGUI.centroid.isChecked()
        self._settings["turnsep"] = self._beamCharGUI.turnsep.isChecked()
        self._settings["energyHist"] = self._beamCharGUI.ehist.isChecked()
        self._settings["intensity"] = self._beamCharGUI.intens.isChecked()
        self._settings["xz"] = self._beamCharGUI.xz.isChecked()

    def callback_apply(self):
        self.apply_settings()
        self._beamCharWindow.close()
        self._parent.send_status("Creating plot(s)...")

        plots = {}
        num = 0

        for dataset in self._selections:

            corrected = {}
            plot_data = {"xRMS": np.array([]), "yRMS": np.array([]), "zRMS": np.array([]),
                         "xHalo": np.array([]), "yHalo": np.array([]), "zHalo": np.array([]),
                         "xCentroid": np.array([]), "yCentroid": np.array([]), "turnSep": np.array([]),
                         "R": np.array([]), "energy": np.array([]), "intensity": np.array([])}

            datasource = dataset.get_datasource()

            nsteps, npart = dataset.get_nsteps(), dataset.get_npart()

            if nsteps > 1:
                # nsteps = int(nsteps - nsteps*(20/420))
                nsteps = 400

            index = 0

            for step in range(nsteps):

                if nsteps > 1:
                    completed = int(100*(step/(nsteps-1)))
                    self._parent.send_status("Plotting progress: {}% complete".format(completed))

                corrected["Step#{}".format(step)] = {}

                x_val = np.array(datasource["Step#{}".format(step)]["x"])
                y_val = np.array(datasource["Step#{}".format(step)]["y"])
                z_val = np.array(datasource["Step#{}".format(step)]["z"])

                px_mean = np.mean(np.array(datasource["Step#{}".format(step)]["px"]))
                py_mean = np.mean(np.array(datasource["Step#{}".format(step)]["py"]))
                theta = np.arccos(py_mean/np.linalg.norm([px_mean, py_mean]))
                if px_mean < 0:
                    theta = -theta

                # Center the beam
                corrected["Step#{}".format(step)]["x"] = x_val - np.mean(x_val)
                corrected["Step#{}".format(step)]["y"] = y_val - np.mean(y_val)
                corrected["Step#{}".format(step)]["z"] = z_val - np.mean(z_val)

                # Rotate the beam
                temp_x = corrected["Step#{}".format(step)]["x"]
                temp_y = corrected["Step#{}".format(step)]["y"]
                corrected["Step#{}".format(step)]["x"] = temp_x*np.cos(theta) - temp_y*np.sin(theta)
                corrected["Step#{}".format(step)]["y"] = temp_x*np.sin(theta) + temp_y*np.cos(theta)

                # Calculate RMS
                if self._settings["rms"]:
                    plot_data["xRMS"] = np.append(plot_data["xRMS"],
                                                  1000.0 * self.rms(corrected["Step#{}".format(step)]["x"]))
                    plot_data["yRMS"] = np.append(plot_data["yRMS"],
                                                  1000.0 * self.rms(corrected["Step#{}".format(step)]["y"]))
                    plot_data["zRMS"] = np.append(plot_data["zRMS"],
                                                  1000.0 * self.rms(corrected["Step#{}".format(step)]["z"]))

                # Calculate halo parameter
                if self._settings["halo"]:
                    plot_data["xHalo"] = np.append(plot_data["xHalo"],
                                                   self.halo(corrected["Step#{}".format(step)]["x"]))
                    plot_data["yHalo"] = np.append(plot_data["yHalo"],
                                                   self.halo(corrected["Step#{}".format(step)]["y"]))
                    plot_data["zHalo"] = np.append(plot_data["zHalo"],
                                                   self.halo(corrected["Step#{}".format(step)]["z"]))

                # Calculate energy
                if self._settings["energyHist"] or self._settings["intensity"]:
                    m_amu = 12791.8548 # Rest mass of simulation macroparticle, in amu
                    m_MeV = 1.19156e07  # Rest mass of simulation macroparticle, in MeV/c^2

                    px_val = np.array(datasource["Step#{}".format(step)]["px"])
                    py_val = np.array(datasource["Step#{}".format(step)]["py"])
                    pz_val = np.array(datasource["Step#{}".format(step)]["pz"])
                    betagamma = np.sqrt(np.square(px_val) + np.square(py_val) + np.square(pz_val))
                    energy = np.sqrt(np.square(betagamma*m_MeV) + np.square(m_MeV))/m_amu
                    # energy = np.sqrt(np.square((np.sqrt(betagamma**2 +1) - 1.0)*m_MeV) + np.square(m_MeV))/m_amu
                    plot_data["energy"] = np.append(plot_data["energy"], energy)
                    # plot_data["energy"] = np.append(plot_data["energy"], energy)

                    if self._settings["intensity"]:
                        pass
                    #TODO Figure out intensity

                # Add centroid coordinates
                if self._settings["centroid"]:
                    plot_data["xCentroid"] = np.append(plot_data["xCentroid"], np.mean(x_val))
                    plot_data["yCentroid"] = np.append(plot_data["yCentroid"], np.mean(y_val))

                if step >= (16 * 95) + 6 and step % 16 == 6 and self._settings["turnsep"]:
                    r = np.sqrt(np.square(np.mean(x_val)) + np.square(np.mean(y_val)))
                    plot_data["R"] = np.append(plot_data["R"], r)
                if step > (16 * 95) + 6 and step % 16 == 6 and self._settings["turnsep"]:
                    index += 1
                    difference = np.abs(plot_data["R"][index-1] - plot_data["R"][index])
                    plot_data["turnSep"] = np.append(plot_data["turnSep"], difference)
            plots["plot_data{}".format(num)] = plot_data
            num += 1

        self._parent.send_status("Saving plot(s)...")

        # Save plots as separate images, with appropriate titles
        linestyles = ['-', '--', '-.']

        if self._settings["rms"]:
            fig = plt.figure()
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            plt.rc('text', usetex=True)
            plt.rc('grid', linestyle=':')

            ax1 = plt.subplot(311)
            plt.title("RMS Beam Size (mm)")
            for n in range(num):
                plt.plot(range(nsteps), plots["plot_data{}".format(n)]["xRMS"], 'k', lw=0.8, ls=linestyles[n % 3])
            ax1.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            ax1.get_yaxis().set_major_formatter(FormatStrFormatter('%.1f'))
            plt.grid()
            plt.ylabel("Horizontal")

            ax2 = plt.subplot(312, sharex=ax1)
            for n in range(num):
                plt.plot(range(nsteps), plots["plot_data{}".format(n)]["yRMS"], 'k', lw=0.8, ls=linestyles[n % 3])
            ax2.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            ax2.get_yaxis().set_major_formatter(FormatStrFormatter('%.1f'))
            plt.grid()
            plt.ylabel("Longitudinal")

            ax3 = plt.subplot(313, sharex=ax1)
            for n in range(num):
                plt.plot(range(nsteps), plots["plot_data{}".format(n)]["zRMS"], 'k', lw=0.8, ls=linestyles[n % 3])
            ax3.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            ax3.get_yaxis().set_major_formatter(FormatStrFormatter('%.1f'))
            plt.grid()
            plt.xlabel("Step")
            plt.ylabel("Vertical")
            fig.tight_layout()
            fig.savefig(self._filename[0] + '_rmsBeamSize.png', dpi=1200)

        if self._settings["halo"]:
            fig = plt.figure()
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            plt.rc('text', usetex=True)
            plt.rc('grid', linestyle=':')

            ax1 = plt.subplot(311)
            plt.title("Halo Parameter")
            for n in range(num):
                plt.plot(range(nsteps), plots["plot_data{}".format(n)]["xHalo"], 'k', lw=0.8, ls=linestyles[n % 3])
            ax1.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            plt.grid()
            plt.ylabel("Horizontal")

            ax2 = plt.subplot(312, sharex=ax1)
            for n in range(num):
                plt.plot(range(nsteps), plots["plot_data{}".format(n)]["yHalo"], 'k', lw=0.8, ls=linestyles[n % 3])
            ax2.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            plt.grid()
            plt.ylabel("Longitudinal")

            ax3 = plt.subplot(313, sharex=ax1)
            for n in range(num):
                plt.plot(range(nsteps), plots["plot_data{}".format(n)]["zHalo"], 'k', lw=0.8, ls=linestyles[n % 3])
            ax3.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            plt.grid()
            plt.xlabel("Step")
            plt.ylabel("Vertical")
            fig.tight_layout()
            fig.savefig(self._filename[0] + '_haloParameter.png', bbox_inches='tight', dpi=1200)

        if self._settings["centroid"]:
            fig = plt.figure()
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            plt.rc('text', usetex=True)
            plt.rc('grid', linestyle=':')

            plt.title("Top-down view of Centroid Position")
            for n in range(num):
                plt.plot(plots["plot_data{}".format(n)]["xCentroid"], plots["plot_data{}".format(n)]["yCentroid"],
                         'ko', ms=0.5)
            ax = plt.gca()
            ax.set_aspect('equal')
            plt.grid()
            plt.xlabel("Horizontal (m)")
            plt.ylabel("Longitudinal (m)")
            fig.tight_layout()
            fig.savefig(self._filename[0] + '_centroidPosition.png', bbox_inches='tight', dpi=1200)

        # TODO: Fix turn separation to allow any number of steps
        if self._settings["turnsep"]:
            fig = plt.figure()
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            plt.rc('text', usetex=True)
            plt.rc('grid', linestyle=':')

            plt.title("Turn Separation")
            plt.plot(range(96, 105), 1000.0 * plot_data["turnSep"], 'k', lw=0.8)
            plt.grid()
            plt.xlabel("Outer Turn")
            plt.ylabel("Separation (mm)")
            fig.savefig(self._filename[0] + '_turnSeparation.png', bbox_inches='tight', dpi=1200)

        if self._settings["energyHist"]:
            fig = plt.figure()
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            plt.rc('text', usetex=True)
            plt.rc('grid', linestyle=':')

            plt.title("Particle Energy")
            plt.hist(plots["plot_data0"]["energy"], 1000, color='k', histtype='step')
            plt.grid()
            plt.xlabel("Energy per Particle (MeV/amu)")
            plt.ylabel(r"Number of $H_2^{+}$ Particles ($\times$6348)")
            fig.tight_layout()
            fig.savefig(self._filename[0] + '_energy.png', bbox_inches='tight', dpi=1200)

        if self._settings["xz"]:
            fig = plt.figure()
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            plt.rc('text', usetex=True)
            plt.rc('grid', linestyle=':')

            plt.title("Probe Scatter Plot")
            ax = plt.gca()
            plt.plot(x_val, z_val, 'ko', alpha=0.6,  markersize=0.005)
            plt.grid()
            ax.set_aspect('equal')
            ax.set_xlim(right=1730)
            plt.xlabel("Horizontal (mm)")
            plt.ylabel("Vertical (mm)")
            fig.tight_layout()
            fig.savefig(self._filename[0] + '_XZ.png', bbox_inches='tight', dpi=1200)

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
