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

    def import_data(self, filename, species):

        # TODO: There is a lot of looping going on, the fewer instructions the better. -PW

        if self._debug:
            print("Importing data from program: {}".format(self._program_name))

        try:

            datasource = {}
            data = {}

            with open(filename, 'rb') as infile:

                _n = 7  # Length of the n-tuples to unpack from the values list
                key_list = ["x", "y", "z", "px", "py", "pz", "E"]  # Things we want to save

                firstline = infile.readline()
                lines = infile.readlines()
                raw_values = [float(item) for item in firstline.strip().split()]
                nsteps = int((len(raw_values) - 1) / _n) # Number of steps
                npart = len(lines) + 1

                # Fill in the values for the first line now
                _id = int(raw_values.pop(0))

                for step in range(nsteps):
                    step_str = "Step#{}".format(step)

                    datasource[step_str] = {}

                    for key in key_list:
                        datasource[step_str][key] = ArrayWrapper(np.zeros(npart))

                    values = raw_values[(step * _n):(_n + step * _n)]

                    gamma = values[6] / species.mass_mev() + 1.0
                    beta = np.sqrt(1.0 - np.power(gamma, -2.0))
                    v_tot = np.sqrt(values[3] ** 2.0 + values[4] ** 2.0 + values[5] ** 2.0)

                    values[0:3] = [r for r in values[0:3]]
                    values[3:6] = [beta * gamma * v / v_tot for v in values[3:6]]  # Convert velocity to momentum

                    for idx, key in enumerate(key_list):
                        datasource[step_str][key][_id - 1] = values[idx]

                # Now for every other line
                for line in lines:

                    raw_values = [float(item) for item in line.strip().split()]  # Data straight from the text file
                    _id = int(raw_values.pop(0))  # Particle ID number

                    for step in range(nsteps):
                        step_str = "Step#{}".format(step)
                        values = raw_values[(step * _n):(_n + step * _n)]

                        gamma = values[6] / species.mass_mev() + 1.0
                        beta = np.sqrt(1.0 - gamma ** (-2.0))
                        v_tot = np.sqrt(values[3] ** 2.0 + values[4] ** 2.0 + values[5] ** 2.0)

                        values[0:3] = [r for r in values[0:3]]
                        values[3:6] = [beta * gamma * v / v_tot for v in values[3:6]]  # Convert velocity to momentum

                        for idx, key in enumerate(key_list):
                            datasource[step_str][key][_id - 1] = values[idx]

                species.calculate_from_energy_mev(datasource["Step#0"]["E"][0])

                data["datasource"] = datasource
                data["ion"] = species
                data["mass"] = species.a()
                data["charge"] = species.q()
                data["steps"] = len(datasource.keys())
                data["current"] = None
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
        ion = dataset.get_ion()
        nsteps = dataset.get_nsteps()
        npart = dataset.get_npart()

        with open(filename + ".txt", "w") as outfile:
            for i in range(npart):
                outstring = "{} ".format(i)
                for step in range(nsteps):
                    _px = datasource.get("Step#{}".format(step)).get("px")[i]
                    _py = datasource.get("Step#{}".format(step)).get("py")[i]
                    _pz = datasource.get("Step#{}".format(step)).get("pz")[i]

                    _vx, _vy, _vz = (clight * _px / np.sqrt(_px ** 2.0 + 1.0),
                                     clight * _py / np.sqrt(_py ** 2.0 + 1.0),
                                     clight * _pz / np.sqrt(_pz ** 2.0 + 1.0))

                    outstring += "{} {} {} {} {} {} {} ".format(datasource.get("Step#{}".format(step)).get("x")[i],
                                                                datasource.get("Step#{}".format(step)).get("y")[i],
                                                                datasource.get("Step#{}".format(step)).get("z")[i],
                                                                _vx, _vy, _vz, ion.energy_mev())
                outfile.write(outstring + "\n")
