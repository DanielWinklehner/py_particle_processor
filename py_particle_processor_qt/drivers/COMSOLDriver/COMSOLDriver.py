from ..arraywrapper import ArrayWrapper
from ..abstractdriver import AbstractDriver
from dans_pymodules import IonSpecies, clight
import numpy as np


class COMSOLDriver(AbstractDriver):
    def __init__(self, debug=False):
        super(COMSOLDriver, self).__init__()
        # TODO: Currently using: (TIME [s], X [m], Y [m], Z [m], VX [m/s], VY [m/s], VZ [m/s], E [MeV])

        self._debug = debug
        self._program_name = "COMSOL"

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
            ion = IonSpecies("H2_1+", 1.0)

            with open(filename, 'rb') as infile:

                # TODO: We may be able to save overall beam parameters into a separate file, but not the header -PW

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

                firstline = infile.readline()
                raw_values = [float(item) for item in firstline.strip().split()]
                nsteps = int(len(raw_values) / _n)  # Number of steps

                # Fill in the values for the first line now
                _id = int(raw_values.pop(0))
                for step in range(nsteps):
                    step_str = "Step#{}".format(step)
                    datasource[step_str] = {}

                    for key in key_list:
                        datasource[step_str][key] = ArrayWrapper(np.zeros(npart))

                    values = raw_values[(1 + step * _n):(_n + step * _n)]

                    # TODO: The energy input is the total energy, not MeV/amu.
                    gamma = values[6] / ion.mass_mev() + 1.0
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

                        gamma = values[6] / ion.mass_mev() + 1.0
                        beta = np.sqrt(1.0 - gamma ** (-2.0))
                        v_tot = np.sqrt(values[3] ** 2.0 + values[4] ** 2.0 + values[5] ** 2.0)

                        values[0:3] = [r for r in values[0:3]]
                        values[3:6] = [beta * gamma * v / v_tot for v in values[3:6]]  # Convert velocity to momentum

                        for idx, key in enumerate(key_list):
                            datasource[step_str][key][_id - 1] = values[idx]

                data["datasource"] = datasource
                data["ion"] = IonSpecies("H2_1+", datasource["Step#0"]["E"][0]) # TODO
                data["mass"] = data["ion"].a()
                data["charge"] = data["ion"].q()
                data["steps"] = len(datasource.keys())
                data["current"] = 0.0
                data["particles"] = len(datasource["Step#0"]["x"])

                if self._debug:
                    print("Found {} steps in the file.".format(data["steps"]))
                    print("Found {} particles in the file.".format(data["particles"]))

                return data

        except Exception as e:

            print("Exception happened during particle loading with {} "
                  "ImportExportDriver: {}".format(self._program_name, e))

        return None

    def export_data(self, dataset, filename):

        if self._debug:
            print("Exporting data for program: {}".format(self._program_name))

        datasource = dataset.get_datasource()
        nsteps = dataset.get_nsteps()
        npart = dataset.get_npart()

        with open(filename + ".txt", "w") as outfile:
            for i in range(npart):
                outstring = ""
                for step in range(nsteps):
                    _px = datasource.get("Step#{}".format(step)).get("px")[i]
                    _py = datasource.get("Step#{}".format(step)).get("py")[i]
                    _pz = datasource.get("Step#{}".format(step)).get("pz")[i]

                    _vx, _vy, _vz = (clight * _px / np.sqrt(_px ** 2.0 + 1.0),
                                     clight * _py / np.sqrt(_py ** 2.0 + 1.0),
                                     clight * _pz / np.sqrt(_pz ** 2.0 + 1.0))

                    outstring += "{} {} {} {} {} {} ".format(datasource.get("Step#{}".format(step)).get("x")[i],
                                                             datasource.get("Step#{}".format(step)).get("y")[i],
                                                             datasource.get("Step#{}".format(step)).get("z")[i],
                                                             _vx, _vy, _vz)
                outfile.write(outstring + "\n")
