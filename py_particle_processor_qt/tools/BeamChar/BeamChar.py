from ..abstract_tool import AbstractTool
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from .beamchargui import Ui_BeamChar
from matplotlib.ticker import LinearLocator, LogLocator
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
        largepos = 1.0e36

        for dataset in self._selections:

            corrected = {}
            name = dataset.get_name()
            nsteps, npart = dataset.get_nsteps(), dataset.get_npart()

            plot_data = {"name": name,
                         "xRMS": np.array([]),
                         "yRMS": np.array([]),
                         "zRMS": np.array([]),
                         "xHalo": np.array([]),
                         "yHalo": np.array([]),
                         "zHalo": np.array([]),
                         "xCentroid": np.ones(nsteps) * largepos,
                         "yCentroid": np.ones(nsteps) * largepos,
                         "turnSep": np.array([]),
                         "R": np.array([]),
                         "energy": np.array([]),
                         "power": np.array([]),
                         "coords": []}

            azimuths = np.ones(nsteps) * largepos
            r_temps = np.ones(nsteps) * largepos

            datasource = dataset.get_datasource()

            index = 0

            save_r = True
            r_tsep = []

            for step in range(nsteps):

                m_amu = 2.01510  # Rest mass of individual H2+, in amu
                m_MeV = 1876.9729554  # Rest mass of individual H2+, in MeV/c^2

                if self._settings["rms"] or self._settings["halo"]:
                    px_val = np.array(datasource["Step#{}".format(step)]["px"])
                    py_val = np.array(datasource["Step#{}".format(step)]["py"])
                    pz_val = np.array(datasource["Step#{}".format(step)]["pz"])
                    betagamma = np.sqrt(np.square(px_val) + np.square(py_val) + np.square(pz_val))
                    energy = np.mean((np.sqrt(np.square(betagamma * m_MeV) + np.square(m_MeV)) - m_MeV) / m_amu)
                    plot_data["energy"] = np.append(plot_data["energy"], energy)

                if nsteps > 1:
                    completed = int(100*(step/(nsteps-1)))
                    self._parent.send_status("Plotting progress: {}% complete".format(completed))

                corrected["Step#{}".format(step)] = {}

                x_val = np.array(datasource["Step#{}".format(step)]["x"])
                y_val = np.array(datasource["Step#{}".format(step)]["y"])
                z_val = np.array(datasource["Step#{}".format(step)]["z"])

                if self._settings["xz"]:

                    r = np.sqrt(np.square(x_val) + np.square(y_val))

                    plot_data["coords"] = np.append(plot_data["coords"], z_val)
                    plot_data["R"] = np.append(plot_data["R"], r)

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
                    m_amu = 2.01510  # Rest mass of individual H2+, in amu
                    m_mev = 1876.9729554  # Rest mass of individual H2+, in MeV/c^2

                    px_val = np.array(datasource["Step#{}".format(step)]["px"])
                    py_val = np.array(datasource["Step#{}".format(step)]["py"])
                    pz_val = np.array(datasource["Step#{}".format(step)]["pz"])

                    betagamma = np.sqrt(np.square(px_val) + np.square(py_val) + np.square(pz_val))
                    energy = (np.sqrt(np.square(betagamma * m_mev) + np.square(m_mev)) - m_mev) / m_amu  # MeV/amu

                    plot_data["energy"] = np.append(plot_data["energy"], energy)

                    if self._settings["intensity"]:

                        q_macro = 1.017 * 1e-15  # fC  --> C
                        f_cyclo = 49.16 * 1.0e6  # MHz --> Hz
                        duty_factor = 0.9  # assumed IsoDAR has 90% duty factor

                        # Power deposition of a single h2+ particle (need to use full energy here!) (W)
                        power = q_macro * f_cyclo * energy * 1e6 * m_amu * duty_factor
                        plot_data["power"] = np.append(plot_data["power"], power)

                        # Radii (m)
                        r = np.sqrt(np.square(x_val) + np.square(y_val))
                        plot_data["R"] = np.append(plot_data["R"], r)

                # Add centroid coordinates
                if self._settings["centroid"] or self._settings["turnsep"]:

                    plot_data["xCentroid"][step] = np.mean(x_val)
                    plot_data["yCentroid"][step] = np.mean(y_val)

                    # Calculate turn separation (as close as possible to pos x-axis for now, arbitrary angle later? -DW)
                    if self._settings["turnsep"]:
                        azimuth = np.rad2deg(np.arctan2(plot_data["yCentroid"][step], plot_data["xCentroid"][step]))
                        azimuths[step] = azimuth
                        r_temp = np.sqrt(np.square(plot_data["xCentroid"][step]) +
                                         np.square(plot_data["yCentroid"][step]))
                        r_temps[step] = r_temp

                        if azimuth > 0 and save_r:
                            save_r = False
                            r_tsep.append(r_temp)
                        if azimuth < 0:
                            save_r = True

                # if step >= (16 * 95) + 6 and step % 16 == 6 and self._settings["turnsep"]:
                #     r = np.sqrt(np.square(np.mean(x_val)) + np.square(np.mean(y_val)))
                #     plot_data["R"] = np.append(plot_data["R"], r)
                # if step > (16 * 95) + 6 and step % 16 == 6 and self._settings["turnsep"]:
                #     index += 1
                #     difference = np.abs(plot_data["R"][index-1] - plot_data["R"][index])
                #     plot_data["turnSep"] = np.append(plot_data["turnSep"], difference)

            plots["plot_data{}".format(num)] = plot_data

            num += 1

        self._parent.send_status("Saving plot(s)...")
        # Save plots as separate images, with appropriate titles

        if self._settings["rms"]:
            fig = plt.figure()
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            plt.rc('text', usetex=True)
            plt.rc('grid', linestyle=':')

            ax1 = plt.subplot(311)
            plt.title("RMS Beam Size (mm)")
            for n in range(num):
                plt.plot(plots["plot_data{}".format(n)]["energy"], plots["plot_data{}".format(n)]["xRMS"], lw=0.8,
                         label=plots["plot_data{}".format(n)]["name"])
                # print("Mean x RMS: {}".format(np.mean(plots["plot_data{}".format(n)]["xRMS"][40:])))
            ax1.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            ax1.get_yaxis().set_major_formatter(FormatStrFormatter('%.1f'))
            # ax1.set_xlim([0,62.25])
            plt.grid()
            plt.ylabel("Horizontal")

            ax2 = plt.subplot(312, sharex=ax1)
            for n in range(num):
                plt.plot(plots["plot_data{}".format(n)]["energy"], plots["plot_data{}".format(n)]["yRMS"], lw=0.8,
                         label=plots["plot_data{}".format(n)]["name"])
                # print("Mean y RMS: {}".format(np.mean(plots["plot_data{}".format(n)]["yRMS"][40:])))
            plt.legend()
            ax2.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            ax2.get_yaxis().set_major_formatter(FormatStrFormatter('%.1f'))
            # ax2.set_xlim([0, 62.25])
            plt.grid()
            plt.ylabel("Longitudinal")

            ax3 = plt.subplot(313, sharex=ax1)
            for n in range(num):
                plt.plot(plots["plot_data{}".format(n)]["energy"], plots["plot_data{}".format(n)]["zRMS"], lw=0.8,
                         label=plots["plot_data{}".format(n)]["name"])
                # print("Mean z RMS: {}".format(np.mean(plots["plot_data{}".format(n)]["zRMS"][40:])))
            ax3.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            ax3.get_yaxis().set_major_formatter(FormatStrFormatter('%.1f'))
            # ax3.set_xlim([0, 62.25])
            plt.grid()
            plt.xlabel("Energy (MeV/amu)")
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
                plt.plot(plots["plot_data{}".format(n)]["energy"], plots["plot_data{}".format(n)]["xHalo"], lw=0.8,
                         label=plots["plot_data{}".format(n)]["name"])
            ax1.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            # ax1.set_xlim([0, 62.25])
            plt.grid()
            plt.ylabel("Horizontal")

            ax2 = plt.subplot(312, sharex=ax1)
            for n in range(num):
                plt.plot(plots["plot_data{}".format(n)]["energy"], plots["plot_data{}".format(n)]["yHalo"], lw=0.8,
                         label=plots["plot_data{}".format(n)]["name"])
            plt.legend()
            ax2.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            # ax2.set_xlim([0, 62.25])
            plt.grid()
            plt.ylabel("Longitudinal")

            ax3 = plt.subplot(313, sharex=ax1)
            for n in range(num):
                plt.plot(plots["plot_data{}".format(n)]["energy"], plots["plot_data{}".format(n)]["zHalo"], lw=0.8,
                         label=plots["plot_data{}".format(n)]["name"])
            ax3.get_yaxis().set_major_locator(LinearLocator(numticks=5))
            # ax3.set_xlim([0, 62.5])
            plt.grid()
            plt.xlabel("Energy (MeV/amu)")
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
                         'o', ms=0.5, label=plots["plot_data{}".format(n)]["name"])
            plt.legend()
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

            plt.plot(1000.0 * np.diff(r_tsep))

            # plt.plot(range(96, 105), 1000.0 * plot_data["turnSep"], 'k', lw=0.8)
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
            for n in range(num):
                plt.hist(plots["plot_data{}".format(n)]["energy"], 1000, histtype='step',
                         weights=np.full_like(plots["plot_data{}".format(n)]["energy"], 6348),
                         label=plots["plot_data{}".format(n)]["name"])
            plt.legend()

            # plt.hist(plots["plot_data0"]["energy"], 1000, color='0.5', histtype='step',
            #          weights=np.full_like(plots["plot_data0"]["energy"], 6348))
            plt.grid()
            plt.xlabel("Energy per Particle (MeV/amu)")
            plt.ylabel(r"Number of $H_2^{+}$ Particles")
            fig.tight_layout()
            fig.savefig(self._filename[0] + '_energy.png', bbox_inches='tight', dpi=1200)

        if self._settings["intensity"]:
            fig = plt.figure()
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            plt.rc('text', usetex=True)
            plt.rc('grid', linestyle=':')

            plt.title("Histogram of the Beam Power (0.5 mm Bins)")

            bin_width = 0.5  # mm

            for n in range(num):

                radii = plots["plot_data{}".format(n)]["R"] * 1.0e3  # m --> mm

                r_len = radii.max() - radii.min()
                n_bins = int(np.round(r_len / bin_width, 0))

                print("Numerical bin width = {:.4f} mm".format(r_len/n_bins))

                power, bins = np.histogram(radii, bins=n_bins, weights=plots["plot_data{}".format(n)]["power"])

                temp_bins = bins[200:-1]
                temp_power = power[200:]

                idx = np.where(temp_bins <= 1910)  # 1940 for Probe25

                temp_bins = temp_bins[idx]
                temp_power = temp_power[idx]

                print("Min R =", temp_bins[np.where(temp_power == np.min(temp_power))], "mm\n")
                print("Min P =", temp_power[np.where(temp_power == np.min(temp_power))], "W\n")

                plt.hist(bins[:-1], bins, weights=power,
                         label=plots["plot_data{}".format(n)]["name"], alpha=0.3, log=True)

            plt.gca().axhline(200.0, linestyle="--", color="black", linewidth=1.0, label="200 W Limit")
            plt.legend(loc=2)
            plt.grid()
            plt.xlabel("Radius (mm)")
            plt.ylabel("Beam Power (W)")
            fig.tight_layout()
            fig.savefig(self._filename[0] + '_power.png', bbox_inches='tight', dpi=1200)

        if self._settings["xz"]:
            fig = plt.figure()
            plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
            plt.rc('text', usetex=True)
            plt.rc('grid', linestyle=':')

            plt.title("Probe Scatter Plot")
            ax = plt.gca()

            for n in range(num):

                plt.plot(plots["plot_data{}".format(n)]["R"] * 1000.0,  # m --> mm
                         plots["plot_data{}".format(n)]["coords"] * 1000.0,  # m --> mm
                         'o', alpha=0.6, markersize=0.005, label=plots["plot_data{}".format(n)]["name"])

            plt.grid()
            ax.set_aspect('equal')
            plt.xlabel("Radius (mm)")
            plt.ylabel("Vertical (mm)")
            fig.tight_layout()
            fig.savefig(self._filename[0] + '_RZ.png', bbox_inches='tight', dpi=1200)

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
