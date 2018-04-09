from ..arraywrapper import ArrayWrapper
from ..abstractdriver import AbstractDriver
from dans_pymodules import IonSpecies
import numpy as np
from scipy import constants as const

clight = const.value("speed of light in vacuum")


class TrackDriver(AbstractDriver):

    def __init__(self, debug=False):
        super(TrackDriver, self).__init__()
        self._debug = debug
        self._program_name = "Track"

    def get_program_name(self):
        return self._program_name

    def import_data(self, filename, species=None):

        if self._debug:
            print("Importing data from program: {}".format(self._program_name))

        try:

            # TODO: All of this should be part of the particle_processor, not the loading driver! -DW
            # Except energy, need that to transform into internal units
            align_bunches = True
            z_center = -0.25  # user decides centroid position (m)
            t_cut = 10.0  # Cut everything above 10 ns away (insufficiently accelerated beam)
            t_split = -10.0  # Split bunches at -10.0 ns and shift leading bunch back
            e_mean_total = 0.07  # MeV

            with open(filename, 'rb') as infile:

                header1 = infile.readline()

                if self._debug:
                    print(header1)

                lines = infile.readlines()

            data = {}
            emean = e_mean_total/species.a()  # MeV/amu  (70 keV)
            # current = 0.01  # mA
            species.calculate_from_energy_mev(emean)

            data["steps"] = 1
            data["ion"] = species
            data["mass"] = data["ion"].a()
            data["charge"] = data["ion"].q()
            # data["current"] = current  # (A)
            data["energy"] = emean * species.a()
            data["particles"] = 0

            npart = len(lines)

            dt = np.zeros(npart)
            dw = np.zeros(npart)
            x = np.zeros(npart)
            xp = np.zeros(npart)
            y = np.zeros(npart)
            yp = np.zeros(npart)

            for i, line in enumerate(lines):
                # Data: Nseed, iq, dt (ns), dW (MeV/amu), x (cm), x' (mrad), y (cm), y' (mrad)
                _, _, dt[i], dw[i], x[i], xp[i], y[i], yp[i] = [float(value) for value in line.strip().split()]

            # Apply cut:
            indices = np.where(dt <= t_cut)

            dt = dt[indices]  # ns
            dw = dw[indices]  # MeV/amu
            x = x[indices] * 1.0e-2  # cm --> m
            xp = xp[indices] * 1.0e-3  # mrad --> rad
            y = y[indices] * 1.0e-2  # cm --> m
            yp = yp[indices] * 1.0e-3  # mrad --> rad

            npart_new = len(x)

            gammaz = (dw + emean) * species.a() / species.mass_mev() + 1.0
            betaz = np.sqrt(1.0 - gammaz**(-2.0))

            pz = gammaz * betaz
            px = pz * np.tan(xp)
            py = pz * np.tan(yp)

            vz = clight * betaz
            # vx = vz * np.tan(xp)
            # vy = vz * np.tan(xp)

            print("Cut {} particles out of {}. Remaining particles: {}".format(npart - npart_new, npart, npart_new))

            if align_bunches:

                # Split bunches
                b1_ind = np.where(dt < t_split)
                b2_ind = np.where(dt >= t_split)

                delta_t_theor = 1.0e9 / 32.8e6  # length of one rf period
                delta_t_sim = np.abs(np.mean(dt[b1_ind]) - np.mean(dt[b2_ind]))

                print("Splitting bunches at t = {} ns. "
                      "Time difference between bunch centers = {} ns. "
                      "One RF period = {} ns.".format(t_split, delta_t_sim, delta_t_theor))

                from matplotlib import pyplot as plt

                # plt.subplot(231)
                # plt.scatter(dt[b1_ind], dw[b1_ind], c="red", s=0.5)
                # plt.scatter(dt[b2_ind], dw[b2_ind], c="blue", s=0.5)
                # plt.xlabel("dt (ns)")
                # plt.ylabel("dW (MeV/amu)")
                # plt.subplot(232)
                # plt.scatter(x[b1_ind], xp[b1_ind], c="red", s=0.5)
                # plt.scatter(x[b2_ind], xp[b2_ind], c="blue", s=0.5)
                # plt.xlabel("x (m)")
                # plt.ylabel("x' (rad)")
                # plt.subplot(233)
                # plt.scatter(y[b1_ind], yp[b1_ind], c="red", s=0.5)
                # plt.scatter(y[b2_ind], yp[b2_ind], c="blue", s=0.5)
                # plt.xlabel("y (m)")
                # plt.ylabel("y' (rad)")

                # Shift leading bunch
                dt[b1_ind] += delta_t_theor
                # x[b1_ind] += vx[b1_ind] * 1.0e-9 * delta_t_theor
                # y[b1_ind] += vy[b1_ind] * 1.0e-9 * delta_t_theor

                # plt.subplot(234)
                # plt.scatter(dt[b1_ind], dw[b1_ind], c="red", s=0.5)
                # plt.scatter(dt[b2_ind], dw[b2_ind], c="blue", s=0.5)
                # plt.xlabel("dt (ns)")
                # plt.ylabel("dW (MeV/amu)")
                # plt.subplot(235)
                # plt.scatter(x[b1_ind], xp[b1_ind], c="red", s=0.5)
                # plt.scatter(x[b2_ind], xp[b2_ind], c="blue", s=0.5)
                # plt.xlabel("x (m)")
                # plt.ylabel("x' (rad)")
                # plt.subplot(236)
                # plt.scatter(y[b1_ind], yp[b1_ind], c="red", s=0.5)
                # plt.scatter(y[b2_ind], yp[b2_ind], c="blue", s=0.5)
                # plt.xlabel("y (m)")
                # plt.ylabel("y' (rad)")
                #
                # plt.tight_layout()
                # plt.show()

            z = z_center - dt * 1e-9 * vz

            distribution = {'x': ArrayWrapper(x),
                            'px': ArrayWrapper(px),
                            'y': ArrayWrapper(y),
                            'py': ArrayWrapper(py),
                            'z': ArrayWrapper(z),
                            'pz': ArrayWrapper(pz)}

            # For a single timestep, we just define a Step#0 entry in a dictionary (supports .get())
            data["datasource"] = {"Step#0": distribution}
            data["particles"] = npart_new

            return data

        except Exception as e:

            print("Exception happened during particle loading with {} "
                  "ImportExportDriver: {}".format(self._program_name, e))

        return None

    def export_data(self, data):

        # TODO

        if self._debug:
            print("Exporting data for program: {}".format(self._program_name))

        print("Export not yet implemented :(")

        return data
