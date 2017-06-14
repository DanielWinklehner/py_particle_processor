# from dans_pymodules import IonSpecies
# import h5py
from dans_pymodules import MyColors
from scipy import constants as const
from py_particle_processor_qt.drivers import *

__author__ = "Daniel Winklehner, Philip Weigel"
__doc__ = """A container that holds a single dataset with 
multiple time steps and multiple particles per time step. If the data
is too large for memory, it is automatically transferred into 
a h5 file on disk to be operated on.
"""

# Initialize some global constants
amu = const.value("atomic mass constant energy equivalent in MeV")
echarge = const.value("elementary charge")
clight = const.value("speed of light in vacuum")

colors = MyColors()


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

    def export_data(self, dataset, filename):
        return self._driver.export_data(dataset=dataset, filename=filename)


class Dataset(object):

    def __init__(self, debug=False):
        self._draw = False
        self._selected = False

        self._datasource = None
        self._filename = None
        self._driver = None
        self._debug = debug
        self._data = None
        self._color = (0.0, 0.0, 0.0)

        self._properties = {"name": None,
                            "ion": None,
                            "multispecies": None,
                            "current": None,
                            "mass": None,
                            "energy": None,
                            "steps": 0,
                            "curstep": None,
                            "charge": None,
                            "particles": None}

        self._native_properties = {}

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
                    print("Exception occurred during closing of datafile: {}".format(e))

                return 1

        return 0

    def color(self):
        return self._color

    def assign_color(self, i):
        self._color = colors[i]

    def export_to_file(self, filename, driver):
        if driver is not None:
            new_ied = ImportExportDriver(driver_name=driver, debug=self._debug)
            new_ied.export_data(dataset=self, filename=filename)
        elif driver is None:
            return 1

    def get_property(self, key):
        return self._properties[key]

    def set_property(self, key, value):
        self._properties[key] = value
        return 0

    def is_native_property(self, key):
        try:
            return self._native_properties[key] == self._properties[key]
        except KeyError:
            return False

    def properties(self):
        return self._properties

    def get_selected(self):
        return self._selected

    def set_selected(self, selected):
        self._selected = selected

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

    def get_particle(self, particle_id, get_color=False):
        particle = {"x": [], "y": [], "z": []}
        max_step = self.get_nsteps()
        color = None

        for step in range(max_step):
            self.set_step_view(step)

            for key in ["x", "y", "z"]:
                dat = self._data.get(key).value[particle_id]

                if np.isnan(dat) or dat == 0.0:  # TODO: A better way to figure out when a particle terminates
                    if get_color == "step":
                        factor = float(step) / float(max_step)
                        color = ((1 - factor) * 255.0, factor * 255.0, 0.0)
                    elif get_color == "random":
                        color = colors[particle_id]
                    return particle, color
                else:
                    particle[key].append(dat)

        if get_color == "step":
            color = (0.0, 255.0, 0.0)
        elif get_color == "random":
            color = colors[particle_id]

        return particle, color

    # noinspection PyUnresolvedReferences
    def get_a(self):
        if type(self._properties) is IonSpecies:
            return self._properties["ion"].a()
        else:
            return None

    def get_current_step(self):
        return self._properties["curstep"]

    def get_datasource(self):
        return self._datasource

    def get_driver(self):
        return self._driver

    def get_filename(self):
        return self._filename

    def get_i(self):
        return self._properties["current"]

    def get_ion(self):
        return self._properties["ion"]

    def get_npart(self):
        return self._properties["particles"]

    def get_nsteps(self):
        return self._properties["steps"]

    # noinspection PyUnresolvedReferences
    def get_q(self):
        if type(self._properties) is IonSpecies:
            return self._properties["ion"].q()
        else:
            return None

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

            # if self._debug:
            #     print("_data is {}".format(_data))

            if _data is not None:

                self._datasource = _data["datasource"]

                for k in _data.keys():
                    print(k)
                    self._properties[k] = _data[k]
                    self._native_properties[k] = _data[k]
                if type(self._properties["ion"]) is IonSpecies:
                    self._properties["name"] = self._properties["ion"].name()
                self.set_step_view(0)
                # self.set_step_view(self._nsteps - 1)

                return 0

        return 1

    def set_step_view(self, step):

        if step > self._properties["steps"]:

            if self._debug:
                print("set_step_view: Requested step {} exceeded max steps of {}!".format(step,
                                                                                          self._properties["steps"]))

            return 1

        self._properties["curstep"] = step
        self._data = self._datasource.get("Step#{}".format(step))

        return 0
