from py_particle_processor_qt.gui.plot_settings import Ui_PlotSettingsWindow
from py_particle_processor_qt.gui.default_plot_settings import Ui_DefaultPlotSettingsWindow
from PyQt5 import QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np

__author__ = "Philip Weigel, Daniel Winklehner"
__doc__ = """Plotting objects and associated GUI objects used in the PyParticleProcessor."""


class PlotObject(object):

    def __init__(self, parent, graphics_view):
        self._parent = parent  # Parent object, which should be a PlotManager
        self._is_shown = False  # A flag raised by showing the plot
        self._is_3d = False  # A flag that determines if the object is a 3D Plot
        self._enabled = True  # A flag indicating the plot is enabled
        self._graphics_view = graphics_view  # The plot's graphics view object to plot to
        self._plot_settings = {}  # The plot settings for this object
        self._datasets = []  # Datasets being shown in the plot

    def add_dataset(self, dataset):

        self._datasets.append(dataset)  # Add the dataset to the list of datasets

        return 0

    def clear(self):
        if self._is_3d:  # Check if it's a 3D plot
            self._graphics_view.items = []  # Clear the items list
            self._graphics_view.update()  # Update the graphics view
        else:
            for data_item in self._graphics_view.listDataItems():  # Loop through each data item
                self._graphics_view.removeItem(data_item)  # Remove the data item from the graphics view
        return 0

    def is_shown(self):
        return self._is_shown  # Returns the shown flag

    def datasets(self):
        return self._datasets  # Return the list of datasets being shown

    def remove_dataset(self, dataset):

        if dataset in self._datasets:  # If the dataset is in the list...
            del self._datasets[self._datasets.index(dataset)]  # Delete it from the list

    def set_plot_settings(self, plot_settings):
        self._plot_settings = plot_settings  # Set the instance settings to the supplied plot settings

        if "is_3d" in plot_settings.keys():  # If this settings is found, check the value
            if plot_settings["is_3d"] == 2:  # 2 --> True
                self._is_3d = True
            else:
                self._is_3d = False
        else:
            self._is_3d = False

    def get_plot_settings(self, translated=False):
        """
        Gets the plot settings used in propertieswindow.
        Translated means using "x", "y", ... instead of 0, 1, 2, ...
        :param translated: 
        :return: 
        """
        if translated is False:
            return self._plot_settings  # Return raw plot settings
        else:
            t_plot_settings = {}  # Create a new dictionary for the translated plot settings
            en_val = [False, None, True]  # Values for the "enable" settings
            combo_val = ["x", "y", "z", "px", "py", "pz"]  # Values for the combo boxes

            for k, v in self._plot_settings.items():  # Get the key and value of each setting
                if "_en" in k or "is" in k:  # If it's an enable setting...
                    t_plot_settings[k] = en_val[v]
                elif "step" in k:  # If it's the step...
                    t_plot_settings[k] = v
                elif v is None:  # If the value is set to None...
                    t_plot_settings[k] = None
                else:  # Else, it's a combo box setting
                    t_plot_settings[k] = combo_val[v]

            return t_plot_settings

    def show(self):

        self._is_shown = False

        t_plot_settings = self.get_plot_settings(translated=True)  # Get the translated settings
        # Set the displayed axes to what the combo box settings were (param_c will be None for a 2D plot)
        axes = t_plot_settings["param_a"], t_plot_settings["param_b"], t_plot_settings["param_c"]
        enabled = t_plot_settings["param_en"]
        step = t_plot_settings["step"]  # Get the step from the settings

        # Check if the plot object is a 3D plot
        if self._is_3d:

            if enabled:

                # Note: since the get_color is set to random, you won't be able to distinguish different datasets
                for dataset in self._datasets:  # Loop through each dataset

                    # Only do a 3D display for data with more than one step and it's enabled
                    if dataset.get_nsteps() > 1 and self._enabled:

                        _grid = False

                        # Loop through each particle
                        for particle_id in range(dataset.get_npart()):
                            # Get the particle data and color for plotting
                            particle, _c = dataset.get_particle(particle_id, get_color="random")
                            # Make an array of the values and transpose it (needed for plotting)
                            pts = np.array([particle.get(axes[0]), particle.get(axes[1]), particle.get(axes[2])]).T
                            # Create a line item of all the points corresponding to this particle
                            plt = pg.opengl.GLLinePlotItem(pos=pts, color=pg.glColor(_c), width=1.,
                                                           antialias=True)
                            # Add the line object to the graphics view
                            self._graphics_view.addItem(plt)

                        if _grid:  # If the grid is enabled for this plot
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

                            # Add the three grids to the graphics view
                            self._graphics_view.addItem(gx)
                            self._graphics_view.addItem(gy)
                            self._graphics_view.addItem(gz)

                        # Set the "camera" distance
                        self._graphics_view.opts["distance"] = 3e-1  # Seems to be a good value for now

                self._is_shown = True

        else:  # If it's not a 3D plot, it's a 2D plot...
            if enabled:

                for dataset in self._datasets:  # Loop through each dataset

                    dataset.set_step_view(step)  # Set the step for the current dataset
                    # Create a scatter plot item using the values and color from the dataset
                    scatter = pg.ScatterPlotItem(x=dataset.get(axes[0]),
                                                 y=dataset.get(axes[1]),
                                                 pen=pg.mkPen(dataset.color()), brush='b', size=1.0, pxMode=True)
                    # Add the scatter plot item to the graphics view
                    self._graphics_view.addItem(scatter)

                    # Create a title for the graph, which is just the axis labels for now
                    # title = axes[0].upper() + "-" + axes[1].upper()
                    # self._graphics_view.setTitle(title)  # Set the title of the graphics view
                    self._graphics_view.repaint()  # Repaint the view

                self._is_shown = True  # Set the shown flag

        return 0


class PlotManager(object):

    def __init__(self, parent, debug=False):
        self._parent = parent
        self._tabs = parent.tabs()  # Tab Widget from the parent
        self._gvs = []  # A list of the graphics views
        self._plot_objects = []  # A list of the plot objects
        self._debug = debug  # Debug flag
        self._screen_size = parent.screen_size()  # Get the screen size from the parent
        self._plot_settings_gui = None  # Used to store the GUI object so it stays in memory while running
        self._current_plot = None  # Which plot is currently showing (None should be default plots)
        self._default_plots = [None, None, None, None]  # A list of the default plot objects
        self._default_plot_settings = {}  # The plot settings for the default plots
        self._initialize_default_plots()  # Initialization of the default plots

    def _initialize_default_plots(self):

        default_gv = self._parent.get_default_graphics_views()  # Get the default graphics views
        self._default_plots = [PlotObject(self, gv) for gv in default_gv]  # Make the plot objects

        return 0

    @staticmethod
    def add_to_plot(dataset, plot_object):

        if dataset not in plot_object.datasets():  # Only add to the plot object if it isn't already in it
            plot_object.add_dataset(dataset)
        else:
            print("This dataset is already in the PlotObject!")

        return 0

    def add_to_current_plot(self, dataset):
        current_index = self._tabs.currentIndex()

        if current_index == 0:  # Catch the condition that the default plots are shown
            self.add_to_default(dataset)
        else:
            plot_object = self._plot_objects[current_index - 1]
            self.add_to_plot(dataset=dataset, plot_object=plot_object)

        return 0

    def add_to_default(self, dataset):

        for plot_object in self._default_plots:  # Add the dataset to all of the default plot objects
            plot_object.add_dataset(dataset)

        return 0

    def apply_default_plot_settings(self, plot_settings, redraw=False):
        # TODO: Better way to do this -PW
        self._default_plot_settings = plot_settings  # Store the plot settings as the default plot settings
        prefix_list = ["tl", "tr", "bl", "3d"]  # Create a list of prefixes
        for idx, plot_object in enumerate(self._default_plots):  # Enumerate through the default plot objects
            new_plot_settings = {"step": plot_settings["step"]}  # Add the step parameter
            for key, val in plot_settings.items():  # Scan through all of the default plot settings
                if prefix_list[idx] in key:  # If the key has the prefix for this plot object...
                    new_key = "param_"+key.split("_")[1]  # Create a new key that will be used by the plot object
                    new_plot_settings[new_key] = val  # Store the value in that new key
            new_plot_settings["param_c"] = None  # Unused parameter for the 2D plots (needed for 3D)
            if idx == 3:  # The third (last) index corresponds to the 3D plot, and by default it's x, y, z
                new_plot_settings["param_a"] = 0  # 0 --> "x"
                new_plot_settings["param_b"] = 1  # 1 --> "y"
                new_plot_settings["param_c"] = 2  # 2 --> "z"
                new_plot_settings["is_3d"] = 2  # 2 --> True
            plot_object.set_plot_settings(new_plot_settings)  # Apply the plot settings for the current object

        if redraw:  # Redraw the plot if the flag is set
            self.redraw_plot()

        return 0

    def default_plot_settings(self, redraw=False):
        # Create the default plot settings GUI, store it in memory, and run it
        self._plot_settings_gui = PlotSettings(self, redraw=redraw, default=True, debug=self._debug)
        self._plot_settings_gui.run()

        return 0

    def get_default_plot_settings(self):
        return self._default_plot_settings  # Returns the default plot settings (untranslated)

    def get_plot_object(self, tab_index):
        if tab_index == 0:  # In the case of the default plots tab
            return self._default_plots  # It returns the list of all the objects
        else:
            return [self._plot_objects[tab_index - 1]]  # Return it in a list

    def has_default_plot_settings(self):
        # Returns True if the settings for the default plots have been set previously
        for plot_object in self._default_plots:
            if len(plot_object.get_plot_settings()) > 0:
                return True

        return False

    def modify_plot(self):

        if self._tabs.currentIndex() == 0:
            self.default_plot_settings(redraw=True)
        else:
            self.plot_settings(new_plot=False)

        return 0

    def new_plot(self):
        self.new_tab()  # Create a new tab for the new plot
        plot_object = PlotObject(parent=self, graphics_view=self._gvs[-1])  # Create a plot object for the new gv
        self._plot_objects.append(plot_object)  # Add this new plot object to the list of plot objects
        self.plot_settings(new_plot=True)  # Open the plot settings for this plot

        return 0

    def new_tab(self):
        # Create a new widget that will be the new tab
        local_tab = QtWidgets.QWidget(parent=self._tabs, flags=self._tabs.windowFlags())

        gl = QtWidgets.QGridLayout(local_tab)  # Create a grid layout
        gl.setContentsMargins(0, 0, 0, 0)
        gl.setSpacing(6)

        self._gvs.append(pg.PlotWidget(local_tab))  # Add the PlotWidget to the list of graphics views

        gl.addWidget(self._gvs[-1])  # Add the grid layout to the newest graphics view

        # Add the new widget to the tabs widget, and give it a name
        self._tabs.addTab(local_tab, "Tab {}".format(self._tabs.count() + 1))

        return 0

    def plot_settings(self, new_plot=False):

        if new_plot is False:
            current_index = self._tabs.currentIndex()  # The current index of the tab widget
            plot_object = self._plot_objects[current_index - 1]  # Find the plot object corresponding to that tab index
            self._plot_settings_gui = PlotSettings(self, plot_object, debug=self._debug)
        else:
            plot_object = self._plot_objects[-1]
            self._plot_settings_gui = PlotSettings(self, plot_object, new_plot=True, debug=self._debug)

        self._plot_settings_gui.run()  # Run the GUI

        return 0

    def redraw_default_plots(self):
        # Clear, then show each plot object in the default plot object list

        for plot_object in self._default_plots:
            plot_object.clear()
            plot_object.show()

        return 0

    def redraw_plot(self):
        current_index = self._tabs.currentIndex()  # Get the current index of the tab widget

        if current_index == 0:  # If it's zero, it's the first tab/default plots
            self.redraw_default_plots()
        else:
            plot_object = self._plot_objects[current_index - 1]  # If not, get the plot object and redraw
            plot_object.clear()
            plot_object.show()

        return 0

    def remove_dataset(self, dataset):

        for plot_object in self._plot_objects:  # Remove the dataset from each plot object
            plot_object.remove_dataset(dataset)  # Note: the method checks to see if the set is in the object

        for default_plot_object in self._default_plots:  # Remove the dataset from each default plot object
            default_plot_object.remove_dataset(dataset)

        return 0

    def remove_plot(self):

        current_index = self._tabs.currentIndex()

        if current_index == 0:
            print("You cannot remove the default plots!")
            return 1
        else:
            self._tabs.setCurrentIndex(current_index - 1)  # This should always exist -PW
            self._tabs.removeTab(current_index)
            del self._plot_objects[current_index - 1]
            del self._gvs[current_index - 1]

        return 0

    def screen_size(self):
        return self._screen_size  # Return the size of the screen

    def set_tab(self, index):
        if index == "last":
            self._tabs.setCurrentIndex(self._tabs.count() - 1)
        elif index == "first":
            self._tabs.setCurrentIndex(0)
        else:
            self._tabs.setCurrentIndex(index)

        return 0


class PlotSettings(object):

    def __init__(self, parent, plot_object=None, redraw=False, default=False, new_plot=False, debug=False):
        self._parent = parent
        self._plot_object = plot_object
        self._debug = debug  # Debug flag
        self._redraw = redraw  # Redraw flag
        self._default = default  # Default flag
        self._new_plot = new_plot  # New Plot flag

        # --- Initialize the GUI --- #
        if self._default:
            self._settings = parent.get_default_plot_settings()  # Get the (possibly) previously set settings

            self._plotSettingsWindow = QtGui.QMainWindow()
            self._plotSettingsWindowGUI = Ui_DefaultPlotSettingsWindow()
            self._plotSettingsWindowGUI.setupUi(self._plotSettingsWindow)
        else:
            self._settings = plot_object.get_plot_settings()  # Get the (possibly) previously set settings of the object

            self._plotSettingsWindow = QtGui.QMainWindow()
            self._plotSettingsWindowGUI = Ui_PlotSettingsWindow()
            self._plotSettingsWindowGUI.setupUi(self._plotSettingsWindow)

        if len(self._settings) > 0:  # If there are settings, then populate the GUI
            self.populate()
        else:  # If not, then apply the ones from the UI file
            self.apply_settings()

        # --- Connections --- #
        self._plotSettingsWindowGUI.apply_button.clicked.connect(self.callback_apply)
        self._plotSettingsWindowGUI.cancel_button.clicked.connect(self.callback_cancel)
        self._plotSettingsWindowGUI.redraw_button.clicked.connect(self.callback_redraw)
        self._plotSettingsWindowGUI.main_label.setText("Plot Settings")

    def apply_settings(self):

        # Step:
        self._settings["step"] = self._plotSettingsWindowGUI.step_input.value()

        # 3D Plot:
        self._settings["3d_en"] = self._plotSettingsWindowGUI.three_d_enabled.checkState()

        if self._default and isinstance(self._plotSettingsWindowGUI, Ui_DefaultPlotSettingsWindow):
            # Top Left:
            self._settings["tl_en"] = self._plotSettingsWindowGUI.tl_enabled.checkState()
            self._settings["tl_a"] = self._plotSettingsWindowGUI.tl_combo_a.currentIndex()
            self._settings["tl_b"] = self._plotSettingsWindowGUI.tl_combo_b.currentIndex()

            # Top Right:
            self._settings["tr_en"] = self._plotSettingsWindowGUI.tr_enabled.checkState()
            self._settings["tr_a"] = self._plotSettingsWindowGUI.tr_combo_a.currentIndex()
            self._settings["tr_b"] = self._plotSettingsWindowGUI.tr_combo_b.currentIndex()

            # Bottom Left:
            self._settings["bl_en"] = self._plotSettingsWindowGUI.bl_enabled.checkState()
            self._settings["bl_a"] = self._plotSettingsWindowGUI.bl_combo_a.currentIndex()
            self._settings["bl_b"] = self._plotSettingsWindowGUI.bl_combo_b.currentIndex()

            # Redraw:
            self._settings["redraw_en"] = self._plotSettingsWindowGUI.redraw_enabled.checkState()

        elif isinstance(self._plotSettingsWindowGUI, Ui_PlotSettingsWindow):
            # Parameters:
            self._settings["param_a"] = self._plotSettingsWindowGUI.param_combo_a.currentIndex()
            self._settings["param_b"] = self._plotSettingsWindowGUI.param_combo_b.currentIndex()
            self._settings["param_c"] = self._plotSettingsWindowGUI.param_combo_c.currentIndex()
            self._settings["param_en"] = self._plotSettingsWindowGUI.param_enabled.checkState()

    def callback_apply(self):
        # Apply the settings in the GUI, then apply them to the plot object
        self.apply_settings()

        if self._default:
            self._parent.apply_default_plot_settings(self.get_settings(), redraw=self._redraw)
        else:
            self._plot_object.set_plot_settings(plot_settings=self.get_settings())

        self._plotSettingsWindow.close()  # Close the GUI

        if self._new_plot is True:
            self._parent.set_tab("last")
        self._parent.redraw_plot()  # Redraw the plot
        return 0

    def callback_cancel(self):

        self._plotSettingsWindow.close()  # Close the window

        return 0

    def callback_redraw(self):
        self.apply_settings()   # Apply the settings to the GUI

        if self._default:
            self._parent.apply_default_plot_settings(self.get_settings())
            self._parent.redraw_default_plots()
        else:
            self._plot_object.apply_plot_settings(plot_settings=self.get_settings())
            self._parent.redraw_plot()  # Redraw the plot

    def get_settings(self):
        return self._settings  # Return the plot settings

    def populate(self):

        # Step:
        self._plotSettingsWindowGUI.step_input.setValue(self._settings["step"])

        # 3D Plot:
        self._plotSettingsWindowGUI.three_d_enabled.setCheckState(self._settings["3d_en"])

        if self._default and isinstance(self._plotSettingsWindowGUI, Ui_DefaultPlotSettingsWindow):
            # Top Left:
            self._plotSettingsWindowGUI.tl_enabled.setCheckState(self._settings["tl_en"])
            self._plotSettingsWindowGUI.tl_combo_a.setCurrentIndex(self._settings["tl_a"])
            self._plotSettingsWindowGUI.tl_combo_b.setCurrentIndex(self._settings["tl_b"])

            # Top Right:
            self._plotSettingsWindowGUI.tr_enabled.setCheckState(self._settings["tr_en"])
            self._plotSettingsWindowGUI.tr_combo_a.setCurrentIndex(self._settings["tr_a"])
            self._plotSettingsWindowGUI.tr_combo_b.setCurrentIndex(self._settings["tr_b"])

            # Bottom Left:
            self._plotSettingsWindowGUI.bl_enabled.setCheckState(self._settings["bl_en"])
            self._plotSettingsWindowGUI.bl_combo_a.setCurrentIndex(self._settings["bl_a"])
            self._plotSettingsWindowGUI.bl_combo_b.setCurrentIndex(self._settings["bl_b"])

            # Redraw:
            self._plotSettingsWindowGUI.redraw_enabled.setCheckState(self._settings["redraw_en"])

        elif isinstance(self._plotSettingsWindowGUI, Ui_PlotSettingsWindow):
            # Parameters:
            self._plotSettingsWindowGUI.param_combo_a.setCurrentIndex(self._settings["param_a"])
            self._plotSettingsWindowGUI.param_combo_b.setCurrentIndex(self._settings["param_b"])
            self._plotSettingsWindowGUI.param_combo_c.setCurrentIndex(self._settings["param_c"])
            self._plotSettingsWindowGUI.param_enabled.setCheckState(self._settings["param_en"])

    def run(self):

        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._plotSettingsWindow.width())
        _y = 0.5 * (screen_size.height() - self._plotSettingsWindow.height())

        # --- Show the GUI --- #
        self._plotSettingsWindow.show()
        self._plotSettingsWindow.move(_x, _y)
