from ..arraywrapper import ArrayWrapper
from ..abstractdriver import AbstractDriver
from dans_pymodules import IonSpecies
import numpy as np


class TraceWinDriver(AbstractDriver):

    def __init__(self, debug=False):
        super(TraceWinDriver, self).__init__()
        self._debug = debug
        self._program_name = "TraceWin"

    def import_data(self, filename, species=None):

        if self._debug:
            print("Importing data from program: {}".format(self._program_name))

        try:

            with open(filename, 'rb') as infile:

                header1 = infile.readline()

                if self._debug:
                    print(header1)

                data = {}

                npart, mass, energy, frequency, current, charge = \
                    [float(item) for item in infile.readline().strip().split()]

                header2 = infile.readline()

                if self._debug:
                    print(header2)

                species.calculate_from_energy_mev(energy)

                data["steps"] = 1
                data["ion"] = species
                data["mass"] = data["ion"].a()
                data["charge"] = data["ion"].q()
                data["current"] = current  # (A)
                data["particles"] = 0

                _distribution = []
                mydtype = [('x', float), ('xp', float),
                           ('y', float), ('yp', float),
                           ('z', float), ('zp', float),
                           ('ph', float), ('t', float),
                           ('e', float), ('l', float)]

                for line in infile.readlines():
                    values = line.strip().split()
                    if int(values[-1]) == 0:
                        data["particles"] += 1
                        _distribution.append(tuple(values))

                _distribution = np.array(_distribution, dtype=mydtype)

                gamma = _distribution['e'] / data["ion"].mass_mev() + 1.0
                beta = np.sqrt(1.0 - gamma**(-2.0))

                distribution = {'x': ArrayWrapper(_distribution['x'] * 0.001),
                                'px': ArrayWrapper(gamma * beta * np.sin(_distribution['xp'] * 0.001)),
                                'y': ArrayWrapper(_distribution['y'] * 0.001),
                                'py': ArrayWrapper(gamma * beta * np.sin(_distribution['yp'] * 0.001)),
                                'z': ArrayWrapper(_distribution['z'] * 0.001)}

                distribution['pz'] = ArrayWrapper(np.sqrt(beta**2.0 * gamma**2.0
                                                          - distribution['px'].value**2.0
                                                          - distribution['py'].value**2.0
                                                          ))

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
