from ..arraywrapper import ArrayWrapper
from dans_pymodules import IonSpecies
import h5py
import numpy as np

class OPALDriver:

    def __init__(self, debug=False):
        self._debug = debug
        self._program_name = "OPAL"

    @property
    def get_program_name(self):
        return self._program_name

    def import_data(self, filename):

        if self._debug:
            print("Importing data from program: {}".format(self._program_name))

        if h5py.is_hdf5(filename):

            if self._debug:
                print("Opening h5 file..."),

            _datasource = h5py.File(filename)

            if self._debug:
                print("Done!")

            if "OPAL_version" in _datasource.attrs.keys():

                data = {"datasource": _datasource}

                if self._debug:
                    print("Loading dataset from h5 file in OPAL format.")

                data["nsteps"] = len(_datasource.items())

                if self._debug:
                    print("Found {} steps in the file.".format(data["nsteps"]))

                _data = _datasource.get("Step#0")

                # TODO: OPAL apparently doesn't save the charge per particle, but per macroparticle without frequency,
                # TODO: we have no way of telling what the species is! Add manual input. And maybe fix OPAL... -DW
                data["ion"] = IonSpecies("proton", _data.attrs["ENERGY"])
                data["current"] = 0.0  # TODO: Get actual current! -DW
                data["npart"] = len(_data.get("x").value)

                return data

        elif ".dat" in filename:

            if self._debug:
                print("Opening OPAL .dat file...")

            data = {}

            with open(filename, 'rb') as infile:
                data["npart"] = int(infile.readline().rstrip().lstrip())
                data["nsteps"] = 1

                _distribution = []
                mydtype = [('x', float), ('xp', float),
                           ('y', float), ('yp', float),
                           ('z', float), ('zp', float)]

                for line in infile.readlines():
                    values = line.strip().split()
                    _distribution.append(tuple(values))

                _distribution = np.array(_distribution, dtype=mydtype)

                distribution = {'x': ArrayWrapper(_distribution['x']),
                                'px': ArrayWrapper(_distribution['xp']),
                                'y': ArrayWrapper(_distribution['y']),
                                'py': ArrayWrapper(_distribution['yp']),
                                'z': ArrayWrapper(_distribution['z']),
                                'pz': ArrayWrapper(_distribution['zp'])}

                # For a single timestep, we just define a Step#0 entry in a dictionary (supports .get())
                data["datasource"] = {"Step#0": distribution}

                # TODO: OPAL apparently doesn't save the charge per particle, but per macroparticle without frequency,
                # TODO: we have no way of telling what the species is! Add manual input. And maybe fix OPAL... -DW
                data["ion"] = IonSpecies("proton", 0.07)  # TODO: Need a good way to get the energy -PW
                data["current"] = 0.0

            return data

        return None

    def export_data(self, data):

        if self._debug:
            print("Exporting data for program: {}".format(self._program_name))

        print("Export not yet implemented :(")

        return data
