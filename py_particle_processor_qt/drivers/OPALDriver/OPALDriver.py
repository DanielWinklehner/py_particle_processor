from ..arraywrapper import ArrayWrapper
from ..abstractdriver import AbstractDriver
from dans_pymodules import IonSpecies
import numpy as np
import h5py


class OPALDriver(AbstractDriver):

    def __init__(self, debug=False):
        super(OPALDriver, self).__init__()
        self._debug = debug
        self._program_name = "OPAL"

    def get_program_name(self):
        return self._program_name

    def import_data(self, filename, species):

        if self._debug:
            print("Importing data from program: {}".format(self._program_name))

        if h5py.is_hdf5(filename):

            if self._debug:
                print("Opening h5 file..."),

            _datasource = h5py.File(filename, "r+")

            if self._debug:
                print("Done!")

            if "OPAL_version" in _datasource.attrs.keys():

                data = {"datasource": _datasource}

                if self._debug:
                    print("Loading dataset from h5 file in OPAL format.")

                data["steps"] = len(_datasource.keys())-1

                if self._debug:
                    print("Found {} steps in the file.".format(data["steps"]))

                _data = _datasource.get("Step#0")

                # for _key in _data.keys():
                #     print(_key)
                #
                # for _key in _data.attrs.keys():
                #     print(_key)

                # TODO: OPAL apparently doesn't save the charge per particle, but per macroparticle without frequency,
                # TODO: we have no way of telling what the species is! Add manual input. And maybe fix OPAL... -DW
                try:
                    species.calculate_from_energy_mev(_data.attrs["ENERGY"])
                except Exception:
                    pass
                data["ion"] = species
                data["mass"] = species.a()
                data["charge"] = species.q()
                data["current"] = None  # TODO: Get actual current! -DW
                data["particles"] = len(_data.get("x").value)

                return data

        elif ".dat" in filename:

            if self._debug:
                print("Opening OPAL .dat file...")

            data = {}

            with open(filename, "rb") as infile:
                data["particles"] = int(infile.readline().rstrip().lstrip())
                data["steps"] = 1

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
                data["current"] = 0.0

            return data

        return None

    def export_data(self, dataset, filename):

        datasource = dataset.get_datasource()
        nsteps = dataset.get_nsteps()
        npart = dataset.get_npart()

        if ".h5" in filename:

            if self._debug:
                print("Exporting data for program: {}...".format(self._program_name))

            outfile = h5py.File(filename, "w")  # The file dialog will make sure they want to overwrite -PW

            m = [dataset.get_ion().mass_mev() for _ in range(npart)]
            q = [dataset.get_ion().q() for _ in range(npart)]
            id_list = [i for i in range(npart)]

            for step in range(nsteps):
                step_str = "Step#{}".format(step)
                step_grp = outfile.create_group(step_str)
                for key in ["x", "y", "z", "px", "py", "pz"]:
                    step_grp.create_dataset(key, data=datasource[step_str][key])
                step_grp.create_dataset("id", data=id_list)
                step_grp.create_dataset("mass", data=m)
                step_grp.create_dataset("q", data=q)
                step_grp.attrs.__setitem__("ENERGY", dataset.get_ion().energy_mev())

            outfile.attrs.__setitem__("OPAL_version", b"OPAL 1.9.0")
            outfile.close()

            if self._debug:
                print("Export successful!")

            return 0

        elif ".dat" in filename:

            if self._debug:
                print("Exporting data for program: {}...".format(self._program_name))

            if nsteps > 1:
                print("The .dat format only supports one step! Using the selected step...")
                step = dataset.get_current_step()
            else:
                step = 0

            # The file dialog will make sure they want to overwrite -PW
            with open(filename, "w") as outfile:
                data = datasource["Step#{}".format(step)]
                outfile.write(str(npart) + "\n")
                for particle in range(npart):
                    outfile.write(str(data["x"][particle]) + "  " +
                                  str(data["px"][particle]) + "  " +
                                  str(data["y"][particle]) + "  " +
                                  str(data["py"][particle]) + "  " +
                                  str(data["z"][particle]) + "  " +
                                  str(data["pz"][particle]) + "\n")

            if self._debug:
                print("Export successful!")

            return 0

        else:

            print("Something went wrong when exporting to: {}".format(self._program_name))

            return 1
