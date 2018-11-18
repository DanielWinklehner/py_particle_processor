from ..abstractdriver import AbstractDriver
import numpy as np
import os


class FreeCADDriver(AbstractDriver):

    def __init__(self, debug=False):
        super(FreeCADDriver, self).__init__()
        self._debug = debug
        self._program_name = "FreeCAD"

    def get_program_name(self):
        return self._program_name

    def import_data(self, filename, species=None):

        if self._debug:
            print("Importing data from program: {}".format(self._program_name))

        print("FreeCAD driver is export-only!")

        return None

    def export_data(self, dataset, filename):

        # TODO: Make number of trajectories and time frequency user input -DW
        ntrj = 1000  # only use 1000 random trajectories
        freq = 5  # only use every 5th step

        if self._debug:
            print("Exporting data for program: {}".format(self._program_name))

        datasource = dataset.get_datasource()
        nsteps = dataset.get_nsteps()
        maxnumpart = len(datasource.get("Step#0").get("x").value)

        _chosen = np.random.choice(maxnumpart, ntrj)

        with open(os.path.splitext(filename)[0] + ".dat", "w") as outfile:

            outfile.write("step, ID, x (m), y (m), z (m)\n")

            for step in range(nsteps):

                if step % freq == 0:

                    _stepdata = datasource.get("Step#{}".format(step))
                    _ids = _stepdata.get("id").value
                    # npart = len(_ids)

                    indices = np.nonzero(np.isin(_ids, _chosen))[0]

                    if self._debug:
                        print("Saving step {} of {}, found {} matching ID's".format(step, nsteps, len(indices)))

                    for i in indices:

                        # if datasource.get("Step#{}".format(step)).get("id")[i] in _chosen:

                        outstring = "{} {} ".format(step, datasource.get("Step#{}".format(step)).get("id")[i])

                        outstring += "{} {} {}\n".format(datasource.get("Step#{}".format(step)).get("x")[i],
                                                         datasource.get("Step#{}".format(step)).get("y")[i],
                                                         datasource.get("Step#{}".format(step)).get("z")[i])

                        outfile.write(outstring)

        return 0
