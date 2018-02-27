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

            with open(filename, 'rb') as infile:

                header1 = infile.readline()

                if self._debug:
                    print(header1)

                data = {}
                Emean = 0.07  # MeV
                current = 0.01 # mA
                species.calculate_from_energy_mev(Emean)

                data["steps"] = 1
                data["ion"] = species
                data["mass"] = data["ion"].a()
                data["charge"] = data["ion"].q()
                data["current"] = current  # (A)
                data["particles"] = 0

                _distribution = []
                mydtype = [('e', float),
                           ('x', float), ('xp', float),
                           ('y', float), ('yp', float),
                           ('z', float), ('zp', float)]

                n_cut = 0
                dt = []

                align_bunches = True
                _z = -0.25  # Shift distribution to _z (m)


                for line in infile.readlines():
                    values = []

                    for v in line.strip().split():
                        values.append(float(v))

                    values[3] += Emean  # Add 70 keV

                    values.append(0.0) # z (placeholder))
                    values.append(0.0) # zp (placeholder)

                    if values[2] > 10.0:
                        n_cut += 1
                    else:
                        _distribution.append(tuple(values[3:10]))
                        dt.append(values[2])
                        data["particles"] += 1

                species.calculate_from_energy_mev(Emean)

                _distribution = np.array(_distribution, dtype=mydtype)
                print("Cut {} particles out of {}. Remaining particles: {}".format(n_cut,data["particles"], data["particles"]-n_cut))

                gamma = _distribution["e"] / data["ion"].mass_mev() + 1.0
                beta = np.sqrt(1.0 - gamma**(-2.0))

                distribution = {'x': ArrayWrapper(_distribution['x'] * 0.01),
                                'px': ArrayWrapper(gamma * beta * np.sin(_distribution['xp'] * 0.001)),
                                'y': ArrayWrapper(_distribution['y'] * 0.01),
                                'py': ArrayWrapper(gamma * beta * np.sin(_distribution['yp'] * 0.001)),
                                'z': ArrayWrapper(_distribution['z'])}

                distribution['pz'] = ArrayWrapper(np.sqrt(beta**2.0 * gamma**2.0
                                                          - distribution['px'].value**2.0
                                                          - distribution['py'].value**2.0
                                                          ))
                _pz = distribution['pz'].value
                _vz =  clight * _pz / gamma

                distribution['z'] = ArrayWrapper(-_vz * np.array(dt) * 1E-9 +_z)  # Reverse direction

                # Now, align the two bunches, post-cut
                lam = 1.0 / 32.8E6 # 1 / f (where f = 32.8 MHz)
                x, px = distribution["x"].value, distribution["px"].value
                y, py = distribution["y"].value, distribution["py"].value
                z, pz = distribution["z"].value, distribution["pz"].value

                vx, vy, vz = clight * px / gamma, clight * py / gamma, clight * pz / gamma

                if align_bunches is True:
                    for i, t in enumerate(dt):
                        if t < -10.0:
                            x[i] -= vx[i] * lam
                            y[i] -= vy[i] * lam
                            z[i] -= vz[i] * lam

                distribution["x"] = ArrayWrapper(x)
                distribution["y"] = ArrayWrapper(y)
                distribution["z"] = ArrayWrapper(z)

                # For a single timestep, we just define a Step#0 entry in a dictionary (supports .get())
                data["datasource"] = {"Step#0": distribution}

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
