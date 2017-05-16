from dans_pymodules import *
import h5py
from drivers import *

__author__ = "Daniel Winklehner"
__doc__ = """A container that holds a single dataset with 
multiple time steps and multiple particles per time step. If the data
is too large for memory, it is automatically transferred into 
a h5 file on disk to be operated on.
"""

# Initialize some global constants
amu = const.value("atomic mass constant energy equivalent in MeV")
echarge = const.value("elementary charge")
clight = const.value("speed of light in vacuum")


class ImportExportDriver(object):
    """
    A thin wrapper around the drivers for importing and exporting particle data
    """
    def __init__(self,
                 driver_name=None):

        self._driver_name = driver_name
        self._driver = None

        self.load_driver()

    def load_driver(self):
        self._driver = driver_mapping[self._driver_name]['driver']()

    def get_driver_name(self):
        return self._driver_name

    def import_data(self, data):
        return self._driver.import_data(data)

    def export_data(self, data):
        return self._driver.export_data(data)


class Dataset(object):

    def __init__(self, debug=False):
        self._datasource = None
        self._filename = None
        self._ion = None
        self._nsteps = 0
        self._multispecies = False
        self._debug = debug
        self._data = None
        self._current = 0.0
        self._npart = 0  # TODO: For now this is the number of particles at step 0. -DW

    def close(self):
        """
        Close the dataset's source and return 
        :return: 
        """
        if self._datasource is not None:

            try:

                self._datasource.close()

            except Exception as e:

                if self._debug:
                    print("Exception occured during closing of datafile: {}".format(e))

                return 1

        return 0

    def get(self, key):
        """
        Returns the values for the currently set step and given key ("x", "y", "z", "px", "py", "pz")
        :return: 
        """

        if key not in ["x", "y", "z", "px", "py", "pz"]:

            if self._debug:
                print("get(key): Key was not one of 'x', 'y', 'z', 'px', 'py', 'pz'")

            return 1

        if self._data is None:

            if self._debug:
                print("get(key): No data loaded yet!")

            return 1

        return self._data.get(key).value

    def get_a(self):
        return self._ion.a()

    def get_filename(self):
        return self._filename

    def get_i(self):
        return self._current

    def get_npart(self):
        return self._npart

    def get_q(self):
        return self._ion.q()

    def load_from_file(self, filename, driver=None):
        """
        Load a dataset from file. If the file is h5 already, don't load into memory.
        Users can write their own drivers but they have to be compliant with the 
        internal structure of datasets.
        
        :param filename:
        :param driver: 
        :return: 
        """
        self._filename = filename

        if driver is not None:
            print("Drivers not yet implemented.")
            return 1

        if h5py.is_hdf5(filename):

            if self._debug:
                print("Opening h5 file..."),

            self._datasource = h5py.File(filename)

            if self._debug:
                print("Done!")

            if "OPAL_version" in self._datasource.attrs.keys():

                if self._debug:
                    print("Loading dataset from h5 file in OPAL format.")

                self._nsteps = len(self._datasource.items())

                if self._debug:
                    print("Found {} steps in the file.".format(self._nsteps))

                self.set_step_view(0)

                # for key in self._data.attrs.keys():
                #     print key, self._data.attrs[key]

                # TODO: OPAL apparently doesn't save the charge per particle, but per macroparticle without frequency,
                # TODO: we have no way of telling what the species is! Add manual input. And maybe fix OPAL... -DW
                self._ion = IonSpecies("proton", self._data.attrs["ENERGY"])
                self._current = 0.0  # TODO: Get actual current! -DW

                self._npart = len(self._data.get("x").value)

        return 0

    def set_step_view(self, step):

        if step > self._nsteps:

            if self._debug:
                print("set_step_view: Requested step {} exceeded max steps of {}!".format(step, self._nsteps))

            return 1

        self._data = self._datasource.get("Step#{}".format(step))

        return 0
