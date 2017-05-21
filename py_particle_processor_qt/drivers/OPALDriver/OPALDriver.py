import h5py
from dans_pymodules import IonSpecies


class OPALDriver:

    def __init__(self, debug=False):
        self._debug = debug
        self._program_name = "OPAL"

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

        return None

    def export_data(self, data):

        if self._debug:
            print("Exporting data for program: {}".format(self._program_name))

        print("Export not yet implemented :(")

        return data
