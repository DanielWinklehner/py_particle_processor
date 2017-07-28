# from dans_pymodules import IonSpecies
# import h5py
from dans_pymodules import *
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

    def __init__(self, driver_name=None, debug=False):

        self._driver_name = driver_name
        self._driver = None
        self._debug = debug

        self.load_driver()

    def load_driver(self):
        self._driver = driver_mapping[self._driver_name]['driver'](debug=self._debug)

    def get_driver_name(self):
        return self._driver_name

    def import_data(self, filename, species):
        return self._driver.import_data(filename, species=species)

    def export_data(self, dataset, filename):
        return self._driver.export_data(dataset=dataset, filename=filename)


class Dataset(object):

    def __init__(self, indices, species, data=None, debug=False):
        self._draw = False
        self._selected = False

        self._datasource = data
        self._filename = None
        self._driver = None
        self._species = species
        self._debug = debug
        self._data = None
        self._color = (0.0, 0.0, 0.0)
        self._indices = indices
        self._orbit = None

        self._properties = {"name": None,
                            "ion": species,
                            "multispecies": None,
                            "current": None,
                            "mass": None,
                            "energy": None,
                            "steps": 0,
                            "curstep": None,
                            "charge": None,
                            "particles": None}

        self._native_properties = {}

        # This will only be true if the data was supplied via a generator
        # Temporary flags for development - PW
        if self._datasource is not None:
            self._is_generated = True
        else:
            self._is_generated = False

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

    def xy_orbit(self, triplet):
        # Uses a triplet of step numbers to find the center of an orbit

        # Source: https://math.stackexchange.com/questions/213658/get-the-equation-of-a-circle-when-given-3-points
        _x, _y = [], []
        for step in triplet:
            self.set_step_view(step)
            _x.append(float(self.get("x")))
            _y.append(float(self.get("y")))

        matrix = np.matrix([[_x[0] ** 2.0 + _y[0] ** 2.0, _x[0], _y[0], 1],
                            [_x[1] ** 2.0 + _y[1] ** 2.0, _x[1], _y[1], 1],
                            [_x[2] ** 2.0 + _y[2] ** 2.0, _x[2], _y[2], 1]])

        m11 = np.linalg.det(np.delete(matrix, 0, 1))
        m12 = np.linalg.det(np.delete(matrix, 1, 1))
        m13 = np.linalg.det(np.delete(matrix, 2, 1))
        m14 = np.linalg.det(np.delete(matrix, 3, 1))

        xc = 0.5 * m12 / m11
        yc = -0.5 * m13 / m11
        r = np.sqrt(xc ** 2.0 + yc ** 2.0 + m14 / m11)

        self._orbit = (xc, yc, r)

        if self._debug:
            print(self._orbit)

        return 0

    def orbit(self):
        return self._orbit

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

        if key not in ["x", "y", "z", "r", "px", "py", "pz", "pr"]:

            if self._debug:
                print("get(key): Key was not one of 'x', 'y', 'z', 'r', 'px', 'py', 'pz', 'pr'")

            return 1

        if self._data is None:

            if self._debug:
                print("get(key): No data loaded yet!")

            return 1

        if key is "r":
            data_x = self._data.get("x").value
            data_y = self._data.get("y").value

            if self._orbit is not None:
                data = np.sqrt((data_x - self._orbit[0]) ** 2.0 + (data_y - self._orbit[1]) ** 2.0)
            else:
                data = np.sqrt(data_x ** 2.0 + data_y ** 2.0)

            return data

        elif key is "pr":

            data_px = self._data.get("px").value
            data_py = self._data.get("py").value
            p = np.sqrt(data_px ** 2.0 + data_py ** 2.0)

            data_x = self._data.get("x").value
            data_y = self._data.get("y").value

            if self._orbit is not None:
                r = np.sqrt((data_x - self._orbit[0]) ** 2.0 + (data_y - self._orbit[1]) ** 2.0)
            else:
                r = np.sqrt(data_x ** 2.0 + data_y ** 2.0)

            factor = (data_px * data_x + data_py * data_y)/(abs(p) * abs(r))

            data = p * factor

            return data

        else:
            data = self._data.get(key)
            return data.value

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
        if isinstance(self._properties, IonSpecies):
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

    def get_name(self):
        return self._properties["name"]

    # noinspection PyUnresolvedReferences
    def get_q(self):
        if isinstance(self._properties, IonSpecies):
            return self._properties["ion"].q()
        else:
            return None

    def indices(self):
        return self._indices

    def load_from_file(self, filename, name, driver=None):
        """
        Load a dataset from file. If the file is h5 already, don't load into memory.
        Users can write their own drivers but they have to be compliant with the 
        internal structure of datasets.
        
        :param filename:
        :param driver:
        :param name: dataset label
        :return: 
        """
        self._driver = driver
        self._filename = filename

        if driver is not None:

            new_ied = ImportExportDriver(driver_name=driver, debug=self._debug)
            _data = new_ied.import_data(self._filename, species=self._species)

            # if self._debug:
            #     print("_data is {}".format(_data))

            if _data is not None:

                self._datasource = _data["datasource"]

                for k in _data.keys():
                    print(k)
                    self._properties[k] = _data[k]
                    self._native_properties[k] = _data[k]
                # if isinstance(self._properties["ion"], IonSpecies):
                #     self._properties["name"] = self._properties["ion"].name()
                #     self._native_properties["name"] = self._properties["ion"].name()
                self._properties["name"] = name
                # self._native_properties["name"] = name
                self.set_step_view(0)
                # self.set_step_view(self._nsteps - 1)

                # print(self._datasource)

                return 0

        return 1

    def set_indices(self, parent_index, index):
        self._indices = (parent_index, index)

    # def set_name(self, name):
    #     self._properties["name"] = name
    #     self._native_properties["name"] = name

    def set_step_view(self, step):

        if step > self._properties["steps"]:

            if self._debug:
                print("set_step_view: Requested step {} exceeded max steps of {}!".format(step,
                                                                                          self._properties["steps"]))

            return 1

        self._properties["curstep"] = step

        self._data = self._datasource.get("Step#{}".format(step))

        return 0
