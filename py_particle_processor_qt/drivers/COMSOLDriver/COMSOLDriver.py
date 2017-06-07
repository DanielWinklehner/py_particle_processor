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
            ion_mev = ion.mass_mev()

            with open(filename, 'rb') as infile:

                # TODO: We may be able to save overall beam parameters into a separate file, but not the header -PW
                # Number of header lines to remove
                _rm = 8

                # Line 1: Model (COMSOL File Name)
                # Line 2: COMSOL Version
                # Line 3: Date
                # Line 4: Dimension
                for _ in range(4):
                    infile.readline()

                # Line 5: Nodes (Number of particles, in our case)
                npart = int(infile.readline().split()[-1])

                # Line 6: Expressions
                # Line 7: Descriptions
                # Line 8: Properties
                for _ in range(3):
                    infile.readline()

                _n = 8  # Length of the n-tuples to unpack from the values list
                key_list = ["x", "y", "z", "px", "py", "pz", "E"]  # Things we want to save

                # TODO: Maybe use the first line to create the values for the rest of the file?
                firstline = infile.readline()
                raw_values = [float(item) for item in firstline.strip().split()]
                nsteps = int(len(raw_values) / _n)  # Number of steps

                for step in range(nsteps):
                    step_str = "Step#{}".format(step)
                    datasource[step_str] = {}
                    for key in key_list:
                        datasource[step_str][key] = ArrayWrapper(np.zeros(npart))

                # Fill in the values for the first line now
                _id = int(raw_values.pop(0))
                for step in range(nsteps):
                    step_str = "Step#{}".format(step)
                    values = raw_values[(1 + step * _n):(_n + step * _n)]

                    gamma = values[6] / ion_mev + 1.0
                    beta = np.sqrt(1.0 - np.power(gamma, -2.0))
                    v_tot = np.sqrt(values[3] ** 2.0 + values[4] ** 2.0 + values[5] ** 2.0)

                    values[0:3] = [r for r in values[0:3]]
                    values[3:6] = [beta * gamma * v / v_tot for v in values[3:6]]  # Convert velocity to momentum

                    for idx, key in enumerate(key_list):
                        datasource[step_str][key][_id - 1] = values[idx]

                # Now for every other line
                for line in infile.readlines():

                    raw_values = [float(item) for item in line.strip().split()]  # Data straight from the text file
                    _id = int(raw_values.pop(0))  # Particle ID number
                    nsteps = int(len(raw_values) / _n)  # Number of steps the particle existed for

                    for step in range(nsteps):
                        step_str = "Step#{}".format(step)
                        values = raw_values[(1 + step * _n):(_n + step * _n)]

                        gamma = values[6] / ion_mev + 1.0
                        beta = np.sqrt(1.0 - gamma ** (-2.0))
                        v_tot = np.sqrt(values[3]**2.0 + values[4]**2.0 + values[5]**2)

                        values[0:3] = [r for r in values[0:3]]
                        values[3:6] = [beta * gamma * v / v_tot for v in values[3:6]]  # Convert velocity to momentum

                        for idx, key in enumerate(key_list):
                            datasource[step_str][key][_id - 1] = values[idx]

                data["datasource"] = datasource
                data["ion"] = IonSpecies("proton", datasource["Step#0"]["E"][0])
                data["nsteps"] = len(datasource.keys())
                data["current"] = 0.0
                data["npart"] = len(datasource["Step#0"]["x"])

                if self._debug:
                    print("Found {} steps in the file.".format(data["nsteps"]))
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
