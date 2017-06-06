from ..arraywrapper import ArrayWrapper
from ..abstractdriver import AbstractDriver
from dans_pymodules import IonSpecies, echarge
import numpy as np

class COMSOLDriver(AbstractDriver):
    def __init__(self, debug=False):
        super(COMSOLDriver, self).__init__()
        # TODO: We should come up with a "standardized" output file format in COMSOL for importing here.
        # TODO: Currently using: (TIME [s], X [m], Y [m], Z [m], VX [m/s], VY [m/s], VZ [m/s], E [MeV])
        # TODO: These units can be changed if needed. -PW

        self._debug = debug
        self._program_name = "COMSOL"

    @property
    def get_program_name(self):
        return self._program_name

    def import_data(self, filename):

        # TODO: There is a lot of looping going on, the less instructions the better. -PW

        if self._debug:
            print("Importing data from program: {}".format(self._program_name))

        try:

            datasource = {}
            data = {}

            # TODO: Need a better way to find the mass and ion species -PW
            ion = IonSpecies("proton", 1.0)
            m = ion.mass_kg()

            with open(filename, 'rb') as infile:

                # TODO: We may be able to save overall beam parameters into a separate file, but not the header -PW
                # Number of header lines to remove
                _rm = 8

                for _ in range(_rm):
                    infile.readline()

                _n = 8  # Length of the n-tuples to unpack from the values list
                key_list = ["x", "y", "z", "px", "py", "pz", "E"]  # Things we want to save

                for line in infile.readlines():

                    raw_values = [float(item) for item in line.strip().split()]  # Data straight from the text file
                    _id = int(raw_values.pop(0))  # Particle ID number
                    num_iter = int(len(raw_values) / _n)  # Number of steps the particle existed for

                    for i in range(num_iter):

                        step_str = "Step#{}".format(i)

                        try:

                            datasource[step_str]

                        except KeyError:

                            datasource[step_str] = dict()

                            for key in key_list:
                                datasource[step_str][key] = ArrayWrapper([])

                        values = raw_values[(1 + i * _n):(_n + i * _n)]

                        values[0:3] = [r for r in values[0:3]]
                        values[3:6] = [m * v for v in values[3:6]]  # Convert velocity to momentum
                        # values[6] = 1.0e-6 * (values[6] / echarge)  # Convert energy from [J] to [MeV]

                        # This will try to add the values for the specified particle id, but there may not be
                        # enough indices appended to the list to access the [id - 1] element
                        #
                        # Since the file reads the IDs in order, this can be simplified since we would just need to
                        # append a new value every time, but this is a more general approach that doesn't require that.
                        try:

                            # Try adding the values
                            for idx, key in enumerate(key_list):
                                datasource[step_str][key][_id - 1] = values[idx]

                        except IndexError:

                            # Get the number of entries that need to be added
                            length = _id - len(datasource[step_str]["x"])

                            for _ in range(length):

                                for key in key_list:
                                    # Append a 0.0 for each key
                                    datasource[step_str][key].append([0.0])

                            # Now that the index exists, add the values
                            for idx, key in enumerate(key_list):
                                datasource[step_str][key][_id - 1] = values[idx]

                data["datasource"] = datasource
                data["ion"] = IonSpecies("proton", datasource["Step#0"]["E"][0])
                data["nsteps"] = len(datasource.keys())
                data["current"] = 0.0
                data["npart"] = len(datasource["Step#0"]["x"])

                if self._debug:
                    print("Found {} steps in the file.".format(data["nsteps"]))

                if self._debug:
                    print("Found {} particles in the file.".format(data["npart"]))

                return data

        except Exception as e:

            print("Exception happened during particle loading with {} "
                  "ImportExportDriver: {}".format(self._program_name, e))

        return None

    def export_data(self, data):

        if self._debug:
            print("Exporting data for program: {}".format(self._program_name))

        print("Export not yet implemented :(")

        return data


if __name__ == '__main__':
    fn = "/home/philip/work/COMSOL/test_data_set.txt"
    A = COMSOLDriver(debug=True).import_data(fn)
    print(A["ion"])
