# from dans_pymodules import IonSpecies
# import h5py
from scipy import constants as const
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
                 driver_name=None,
                 debug=False):

        self._driver_name = driver_name
        self._driver = None
        self._debug = debug

        self.load_driver()

    def load_driver(self):
        self._driver = driver_mapping[self._driver_name]['driver'](debug=self._debug)

    def get_driver_name(self):
        return self._driver_name

    def import_data(self, filename):
        return self._driver.import_data(filename)

    def export_data(self, data):
        return self._driver.export_data(data)


class Dataset(object):

    def __init__(self, debug=False):
        self._draw = False
        self._datasource = None
        self._filename = None
        self._driver = None
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

    def get_draw(self):
        return self._draw

    def set_draw(self, draw):
        self._draw = draw

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
        self._driver = driver
        self._filename = filename

        if driver is not None:

            new_ied = ImportExportDriver(driver_name=driver, debug=self._debug)
            _data = new_ied.import_data(self._filename)

            print("_data is {}".format(_data))

            if _data is not None:

                self._datasource = _data["datasource"]
                self._ion = _data["ion"]
                self._nsteps = _data["nsteps"]
                self._current = _data["current"]
                self._npart = _data["npart"]

                self.set_step_view(0)

                return 0

        return 1

    def set_step_view(self, step):

        if step > self._nsteps:

            if self._debug:
                print("set_step_view: Requested step {} exceeded max steps of {}!".format(step, self._nsteps))

            return 1

        self._data = self._datasource.get("Step#{}".format(step))

        return 0
