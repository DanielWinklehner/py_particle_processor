from py_particle_processor_qt.gui.plot_settings import Ui_PlotSettingsWindow
from py_particle_processor_qt.gui.default_plot_settings import Ui_DefaultPlotSettingsWindow
from PyQt5 import QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np

# TODO: Debug prints are old


class PlotObject(object):

    def __init__(self, parent, graphics_view):
        self._parent = parent  # This should always be a PlotManager
        self._is_shown = False
        self._is_3d = False
        self._enabled = False
        self._graphics_view = graphics_view
        self._plot_settings = {}
        self._datasets = []  # Data shown in the plot

        # if len(axes) == 2:
        #     self._is_3d = False
        # elif len(axes) == 3:
        #     self._is_3d = True
        # else:
        #     print("You can only select two or three axes to plot.")

    def add_dataset(self, dataset):

        self._datasets.append(dataset)

        return 0

    def clear(self):

        if self._is_3d:
            self._graphics_view.items = []
            self._graphics_view.update()
        else:
            for data_item in self._graphics_view.listDataItems():
                self._graphics_view.removeItem(data_item)

        return 0

    def is_shown(self):
        return self._is_shown

    def datasets(self):
        return self._datasets

    def remove_dataset(self, dataset):
        if dataset in self._datasets:
            del self._datasets[self._datasets.index(dataset)]

    def set_plot_settings(self, plot_settings):
        self._plot_settings = plot_settings

        if "is_3d" in plot_settings.keys():
            if plot_settings["is_3d"] == 2:
                self._is_3d = True
            else:
                self._is_3d = False
        else:
            self._is_3d = False

        if "param_en" in plot_settings.keys():
            if plot_settings["param_en"]:
                self._enabled = True
            else:
                self._enabled = False
        else:
            self._enabled = False

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
                if "_en" in k or "is" in k:
                    t_plot_settings[k] = en_val[v]
                elif "step" in k:
                    t_plot_settings[k] = v
                elif v is None:
                    t_plot_settings[k] = None
                else:
                    t_plot_settings[k] = combo_val[v]

            return t_plot_settings

    def show(self):

        t_plot_settings = self.get_plot_settings(translated=True)
        axes = t_plot_settings["param_a"], t_plot_settings["param_b"], t_plot_settings["param_c"]
        step = t_plot_settings["step"]

        if self._is_3d:

            # TODO: 3D Plotting, this is from the previous redraw() fucntion

            for dataset in self._datasets:

                # Only do a 3D display for data with more than one step and it's enabled
                if dataset.get_nsteps() > 1 and self._enabled:

                    _grid = True  # Always display the grids for now

                    for particle_id in range(dataset.get_npart()):
                        particle, _c = dataset.get_particle(particle_id, get_color="random")
                        pts = np.array([particle.get(axes[0]), particle.get(axes[1]), particle.get(axes[2])]).T
                        plt = pg.opengl.GLLinePlotItem(pos=pts, color=pg.glColor(_c), width=1.,
                                                       antialias=True)

                        self._graphics_view.addItem(plt)

                    if _grid:
                        # TODO: Make the grid size dynamic -PW
                        # TODO: The maximum and minimum values might be useful to get during import -PW

                        gx = pg.opengl.GLGridItem()
                        gx.rotate(90, 0, 1, 0)
                        gx.translate(0.0, 0.0, 0.0)
                        gx.setSize(x=0.2, y=0.2, z=0.2)
                        gx.setSpacing(x=0.01, y=0.01, z=0.01)

                        gy = pg.opengl.GLGridItem()
                        gy.rotate(90, 1, 0, 0)
                        gy.translate(0.0, 0.0, 0.0)
                        gy.setSize(x=0.2, y=0.2, z=0.2)
                        gy.setSpacing(x=0.01, y=0.01, z=0.01)

                        gz = pg.opengl.GLGridItem()
                        gz.translate(0.0, 0.0, 0.0)
                        gz.setSize(x=0.2, y=0.2, z=1.0)
                        gz.setSpacing(x=0.01, y=0.01, z=0.01)

                        self._graphics_view.addItem(gx)
                        self._graphics_view.addItem(gy)
                        self._graphics_view.addItem(gz)

                    self._graphics_view.opts["distance"] = 3e-1  # Seems to be a good value for now

        else:

            # TODO: We should make sure that the "axes" are in the dataset first -PW
            for dataset in self._datasets:

                dataset.set_step_view(step)

                scatter = pg.ScatterPlotItem(x=dataset.get(axes[0]),
                                             y=dataset.get(axes[1]),
                                             pen=pg.mkPen(dataset.color()), brush='b', size=1.0, pxMode=True)

                self._graphics_view.addItem(scatter)

                title = axes[0].upper() + "-" + axes[1].upper()
                self._graphics_view.setTitle(title)
                self._graphics_view.repaint()

            self._is_shown = True

        return 0


class PlotManager(object):

    def __init__(self, parent, debug=False):
        self._parent = parent
        self._tabs = parent.tabs()
        self._gvs = []
        self._plot_objects = []
        self._debug = debug
        self._screen_size = parent.screen_size()
        self._plot_settings = None
        self._current_plot = None
        self._default_plots = [None, None, None, None]
        self._default_plot_settings = {}
        self._initialize_default_plots()

    def _initialize_default_plots(self):
        # TODO: Better way to do this -PW
        default_gv = (self._parent._mainWindowGUI.graphicsView_1,
                      self._parent._mainWindowGUI.graphicsView_2,
                      self._parent._mainWindowGUI.graphicsView_3,
                      self._parent._mainWindowGUI.graphicsView_4)
        self._default_plots = [PlotObject(self, gv) for gv in default_gv]

    def add_to_plot(self, dataset, plot_object):
        if dataset not in plot_object.datasets():
            plot_object.add_dataset(dataset)
        else:
            print("This dataset is already in the PlotObject!")

    def add_to_current_plot(self, dataset):
        if self._current_plot is None:
            self.add_to_default(dataset)
        else:
            self.add_to_plot(dataset, self._current_plot)

    def add_to_default(self, dataset):
        for plot_object in self._default_plots:
            plot_object.add_dataset(dataset)

    def apply_default_plot_settings(self, plot_settings, redraw=False):
        # TODO: Better way to do this -PW
        self._default_plot_settings = plot_settings
        plot_list = ["tl", "tr", "bl", "3d"]
        for idx, plot_object in enumerate(self._default_plots):
            new_plot_settings = {"step": plot_settings["step"]}
            for key, val in plot_settings.items():
                if plot_list[idx] in key:
                    new_key = "param_"+key.split("_")[1]
                    new_plot_settings[new_key] = val
            new_plot_settings["param_c"] = None
            if idx == 3:
                new_plot_settings["param_a"] = 0
                new_plot_settings["param_b"] = 1
                new_plot_settings["param_c"] = 2
                new_plot_settings["is_3d"] = 2
            plot_object.set_plot_settings(new_plot_settings)

        if redraw:
            self.redraw_plot()

    def clear_plot(self):
        pass

    def get_default_plot_settings(self):
        return self._default_plot_settings

    def has_default_settings(self):

        for plot_object in self._default_plots:
            if len(plot_object.get_plot_settings()) > 0:
                return True

        return False

    def modify_plot(self):
        pass

    def new_plot(self):
        self.new_tab()
        plot_object = PlotObject(parent=self, graphics_view=self._gvs[-1])
        self._plot_objects.append(plot_object)  # Object and tab index encoded (i - 2?)
        self.plot_settings(plot_object)
        pass

    def new_tab(self):
        local_tab = QtWidgets.QWidget(parent=self._tabs, flags=self._tabs.windowFlags())

        gl = QtWidgets.QGridLayout(local_tab)  # TODO: Send this to the PlotObject? -PW
        gl.setContentsMargins(11, 11, 11, 11)
        gl.setSpacing(6)

        self._gvs.append(pg.PlotWidget(local_tab))

        gl.addWidget(self._gvs[-1])

        self._tabs.addTab(local_tab, "Tab GV")
        # To ge the index, we may be able to use: idx = self._tabs.indexOf(local_tab)

    def plot_settings(self, plot_object):
        self._plot_settings = PlotSettings(self, plot_object, debug=self._debug)
        self._plot_settings.run()

    def redraw_plot(self):
        current_index = self._tabs.currentIndex()
        if current_index == 0:
            self.redraw_default_plots()
        else:
            plot_object = self._plot_objects[current_index - 1]
            plot_object.clear()
            plot_object.show()

    def remove_dataset(self, dataset):
        for plot_object in self._plot_objects:
            plot_object.remove_dataset(dataset)

        for default_plot_object in self._default_plots:
            default_plot_object.remove_dataset(dataset)

    def remove_plot(self):
        # TODO: GUI for removing plots, it should find which tab/GV it's in -PW
        # if dataset in self._gvs[gv_i].datasets():
        #     self._gvs[gv_i].remove_dataset(dataset)
        # else:
        #     print("This dataset is not in the PlotObject!")
        pass

    def screen_size(self):
        return self._screen_size

    def redraw_default_plots(self):
        for plot_object in self._default_plots:
            plot_object.clear()
            plot_object.show()

    def default_plot_settings(self, redraw=False):
        self._plot_settings = DefaultPlotSettings(self, redraw=redraw, debug=self._debug)
        self._plot_settings.run()


class DefaultPlotSettings(object):

    def __init__(self, parent, redraw=False, debug=False):
        self._settings = parent.get_default_plot_settings()
        self._debug = debug
        self._parent = parent
        self._redraw = redraw

        self._defaultPlotSettingsWindow = QtGui.QMainWindow()
        self._defaultPlotSettingsWindowGUI = Ui_DefaultPlotSettingsWindow()
        self._defaultPlotSettingsWindowGUI.setupUi(self._defaultPlotSettingsWindow)

        if len(self._settings) > 0:
            self.populate_settings()
        else:
            self.apply_settings()

        self._defaultPlotSettingsWindowGUI.apply_button.clicked.connect(self.callback_apply)
        self._defaultPlotSettingsWindowGUI.cancel_button.clicked.connect(self.callback_cancel)
        self._defaultPlotSettingsWindowGUI.redraw_button.clicked.connect(self.callback_redraw)
        self._defaultPlotSettingsWindowGUI.dataset_label.setText("Default Plot Settings")

    def apply_settings(self):

        if self._debug:
            print("DEBUG: retrieve_settings called")

        # Step:
        self._settings["step"] = self._defaultPlotSettingsWindowGUI.step_input.value()

        # Top Left:
        self._settings["tl_en"] = self._defaultPlotSettingsWindowGUI.tl_enabled.checkState()
        self._settings["tl_a"] = self._defaultPlotSettingsWindowGUI.tl_combo_a.currentIndex()
        self._settings["tl_b"] = self._defaultPlotSettingsWindowGUI.tl_combo_b.currentIndex()

        # Top Right:
        self._settings["tr_en"] = self._defaultPlotSettingsWindowGUI.tr_enabled.checkState()
        self._settings["tr_a"] = self._defaultPlotSettingsWindowGUI.tr_combo_a.currentIndex()
        self._settings["tr_b"] = self._defaultPlotSettingsWindowGUI.tr_combo_b.currentIndex()

        # Bottom Left:
        self._settings["bl_en"] = self._defaultPlotSettingsWindowGUI.bl_enabled.checkState()
        self._settings["bl_a"] = self._defaultPlotSettingsWindowGUI.bl_combo_a.currentIndex()
        self._settings["bl_b"] = self._defaultPlotSettingsWindowGUI.bl_combo_b.currentIndex()

        # 3D Plot:
        self._settings["3d_en"] = self._defaultPlotSettingsWindowGUI.three_d_enabled.checkState()

        # Redraw:
        self._settings["redraw_en"] = self._defaultPlotSettingsWindowGUI.redraw_enabled.checkState()

    def callback_apply(self):

        if self._debug:
            print("DEBUG: callback_apply called")

        self.apply_settings()
        self._parent.apply_default_plot_settings(self.get_settings(), redraw=self._redraw)
        self._defaultPlotSettingsWindow.close()

        return 0

    def callback_cancel(self):

        if self._debug:
            print("DEBUG: callback_cancel called")

        self._defaultPlotSettingsWindow.close()

        return 0

    def callback_redraw(self):
        self.apply_settings()
        self._parent.apply_default_plot_settings(self.get_settings())
        self._parent.redraw_default_plots()

    def get_settings(self):
        return self._settings

    def populate_settings(self):

        if self._debug:
            print("DEBUG: populate_settings called")

        # Step:
        self._defaultPlotSettingsWindowGUI.step_input.setValue(self._settings["step"])

        # Top Left:
        self._defaultPlotSettingsWindowGUI.tl_enabled.setCheckState(self._settings["tl_en"])
        self._defaultPlotSettingsWindowGUI.tl_combo_a.setCurrentIndex(self._settings["tl_a"])
        self._defaultPlotSettingsWindowGUI.tl_combo_b.setCurrentIndex(self._settings["tl_b"])

        # Top Right:
        self._defaultPlotSettingsWindowGUI.tr_enabled.setCheckState(self._settings["tr_en"])
        self._defaultPlotSettingsWindowGUI.tr_combo_a.setCurrentIndex(self._settings["tr_a"])
        self._defaultPlotSettingsWindowGUI.tr_combo_b.setCurrentIndex(self._settings["tr_b"])

        # Bottom Left:
        self._defaultPlotSettingsWindowGUI.bl_enabled.setCheckState(self._settings["bl_en"])
        self._defaultPlotSettingsWindowGUI.bl_combo_a.setCurrentIndex(self._settings["bl_a"])
        self._defaultPlotSettingsWindowGUI.bl_combo_b.setCurrentIndex(self._settings["bl_b"])

        # 3D Plot:
        self._defaultPlotSettingsWindowGUI.three_d_enabled.setCheckState(self._settings["3d_en"])

        # Redraw:
        self._defaultPlotSettingsWindowGUI.redraw_enabled.setCheckState(self._settings["redraw_en"])

    def run(self):

        if self._debug:
            print("DEBUG: Running PlotPropertiesManager")

        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._defaultPlotSettingsWindow.width())
        _y = 0.5 * (screen_size.height() - self._defaultPlotSettingsWindow.height())

        # --- Show the GUI --- #
        self._defaultPlotSettingsWindow.show()
        self._defaultPlotSettingsWindow.move(_x, _y)


class PlotSettings(object):

    def __init__(self, parent, plot_object, debug=False):
        self._parent = parent
        self._plot_object = plot_object
        self._settings = plot_object.get_plot_settings()
        self._debug = debug

        self._plotSettingsWindow = QtGui.QMainWindow()
        self._plotSettingsWindowGUI = Ui_PlotSettingsWindow()
        self._plotSettingsWindowGUI.setupUi(self._plotSettingsWindow)

        if len(self._settings) > 0:
            self.populate_settings()
        else:
            self.apply_settings()

        self._plotSettingsWindowGUI.apply_button.clicked.connect(self.callback_apply)
        self._plotSettingsWindowGUI.cancel_button.clicked.connect(self.callback_cancel)
        self._plotSettingsWindowGUI.redraw_button.clicked.connect(self.callback_redraw)
        self._plotSettingsWindowGUI.main_label.setText("Plot Settings")

    def apply_settings(self):

        # Step:
        self._settings["step"] = self._plotSettingsWindowGUI.step_input.value()

        # 3D Plot:
        self._settings["3d_en"] = self._plotSettingsWindowGUI.three_d_enabled.checkState()

        # Parameters:
        self._settings["param_a"] = self._plotSettingsWindowGUI.param_combo_a.currentIndex()
        self._settings["param_b"] = self._plotSettingsWindowGUI.param_combo_b.currentIndex()
        self._settings["param_c"] = self._plotSettingsWindowGUI.param_combo_c.currentIndex()

        # Redraw:
        self._settings["redraw_en"] = self._plotSettingsWindowGUI.redraw_enabled.checkState()

    def callback_apply(self):

        if self._debug:
            print("DEBUG: callback_apply called")

        self.apply_settings()
        self._plot_object.set_plot_settings(plot_settings=self.get_settings())
        self._plot_object.show()
        self._plotSettingsWindow.close()
        self._parent.redraw_plot()
        return 0

    def callback_cancel(self):

        if self._debug:
            print("DEBUG: callback_cancel called")

        self._plotSettingsWindow.close()

        return 0

    def callback_redraw(self):
        self.apply_settings()
        self._plot_object.apply_plot_settings(plot_settings=self.get_settings())
        self._plot_object.show()

    def get_settings(self):
        return self._settings

    def populate_settings(self):

        if self._debug:
            print("DEBUG: populate_settings called")

        # Step:
        self._plotSettingsWindowGUI.step_input.setValue(self._settings["step"])

        # 3D Plot:
        self._plotSettingsWindowGUI.three_d_enabled.setCheckState(self._settings["3d_en"])

        # Parameters:
        self._plotSettingsWindowGUI.param_combo_a.setCurrentIndex(self._settings["param_combo_a"])
        self._plotSettingsWindowGUI.param_combo_b.setCurrentIndex(self._settings["param_combo_b"])
        self._plotSettingsWindowGUI.param_combo_c.setCurrentIndex(self._settings["param_combo_c"])

        # Redraw:
        self._plotSettingsWindowGUI.redraw_enabled.setCheckState(self._settings["redraw_en"])

    def run(self):

        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._plotSettingsWindow.width())
        _y = 0.5 * (screen_size.height() - self._plotSettingsWindow.height())

        # --- Show the GUI --- #
        self._plotSettingsWindow.show()
        self._plotSettingsWindow.move(_x, _y)
