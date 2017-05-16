# import h5py
from dans_pymodules import IonSpecies
import numpy as np


class ArrayWrapper(object):

    def __init__(self, array_like):

        self._array = np.array(array_like)

    @property
    def value(self):
        return self._array


class TraceWinDriver:

    def __init__(self, debug=False):
        self._debug = debug
        self._program_name = "TraceWin"

    def get_program_name(self):
        return self._program_name

    def import_data(self, filename):

        if self._debug:
            print("Importing data from program: {}".format(self._program_name))

        try:

            with open(filename, 'rb') as infile:

                header1 = infile.readline()

                if self._debug:
                    print(header1)

                data = {}

                npart, mass, energy, frequency, current, charge = \
                    [float(item) for item in infile.readline.strip().split()]

                header2 = infile.readline()

                if self._debug:
                    print(header2)

                data["nsteps"] = 1
                data["ion"] = IonSpecies('H2_1+', energy)  # TODO: Actual ion species! -DW
                data["current"] = current  # (A)
                data["npart"] = 0

                _distribution = []
                mydtype = [('x', float), ('xp', float), ('y', float), ('yp', float), ('z', float), ('zp', float)]

                for line in infile.readlines():
                    values = line.strip().split()
                    if values[-1] == "0":
                        data["npart"] += 1
                        _distribution.append(tuple(values[:6]))

                _distribution = np.array(_distribution, dtype=mydtype)
                print _distribution[:5]

                distribution = {'x': ArrayWrapper(_distribution['x']),
                                'xp': ArrayWrapper(_distribution['xp']),
                                'y': ArrayWrapper(_distribution['y']),
                                'yp': ArrayWrapper(_distribution['yp']),
                                'z': ArrayWrapper(_distribution['z']),
                                'zp': ArrayWrapper(_distribution['zp'])}

                # For a single timestep, we just define a Step#0 entry in a dictionary (supports .get())
                data["datasource"] = {"Step#0": distribution}

                return None

        except Exception as e:

            print("Exception happened during particle loading with {} "
                  "ImportExportDriver: {}".format(self._program_name, e))

        return None

    def export_data(self, data):

        if self._debug:
            print("Exporting data for program: {}".format(self._program_name))

        print("Export not yet implemented :(")

        return data
