# from dans_pymodules import IonSpecies
# import h5py
from dans_pymodules import MyColors
from scipy import constants as const
from py_particle_processor_qt.drivers import *

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

    def export_data(self, data):
        return self._driver.export_data(data)


class Dataset(object):

    def __init__(self, debug=False):
        self._draw = False
        self._selected = False

        self._datasource = None
        self._filename = None
        self._driver = None
        self._debug = debug
        self._data = None
        self._plot_settings = {}

        self._ion = None
        self._multispecies = False
        self._current = 0.0
        self._nsteps = 0
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
                    print("Exception occurred during closing of datafile: {}".format(e))

                return 1

        return 0

    def export_to_file(self, filename, driver):
        if driver is not None:
            new_ied = ImportExportDriver(driver_name=driver, debug=self._debug)
            new_ied.export_data(data=self._data)

    def get_draw(self):
        return self._draw

    def set_draw(self, draw):
        self._draw = draw

    def get_selected(self):
        return self._selected

    def set_selected(self, selected):
        self._selected = selected

    def get_plot_settings(self, translated=False):
        """
        Gets the plot settings used in propertieswindow.
        Translated means using "x", "y", ... instead of 0, 1, 2, ...
        :param translated: 
        :return: 
        """
        if translated is False:
            return self._plot_settings
        else:
            t_plot_settings = {}
            en_val = [False, None, True]
            combo_val = ["x", "y", "z", "px", "py", "pz"]
            for k, v in self._plot_settings.items():
                if "_en" in k:
                    t_plot_settings[k] = en_val[v]
                elif "step" in k:
                    t_plot_settings[k] = v
                else:
                    t_plot_settings[k] = combo_val[v]
            return t_plot_settings

    def set_plot_settings(self, plot_settings):
        self._plot_settings = plot_settings

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
                if np.isnan(dat) or dat == 0.0:  # TODO: This
                    if get_color == "step":
                        factor = float(step) / float(max_step)
                        color = ((1 - factor) * 255.0, factor * 255.0, 0.0)
                    elif get_color == "random":
                        color = colors[particle_id]
                    return particle, color
                else:
                    particle[key].append(dat)
        if get_color == "step":  # TODO: Temporary
            color = (0.0, 255.0, 0.0)
        elif get_color == "random":
            color = colors[particle_id]
        return particle, color

    def get_a(self):
        return self._ion.a()

    def get_driver(self):
        return self._driver

    def get_filename(self):
        return self._filename

    def get_i(self):
        return self._current

    def get_npart(self):
        return self._npart

    def get_nsteps(self):
        return self._nsteps

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
                # self.set_step_view(self._nsteps - 1)

                return 0

        return 1

    def set_step_view(self, step):

        if step > self._nsteps:

            if self._debug:
                print("set_step_view: Requested step {} exceeded max steps of {}!".format(step, self._nsteps))

            return 1

        self._data = self._datasource.get("Step#{}".format(step))

        return 0
