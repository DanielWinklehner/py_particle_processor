from py_particle_processor_qt.dataset import *
from py_particle_processor_qt.gui.main_window import *
from py_particle_processor_qt.gui.species_prompt import *
from py_particle_processor_qt.plotting import *
from py_particle_processor_qt.generator import *
from py_particle_processor_qt.tools import *
from PyQt5.QtWidgets import qApp, QFileDialog

# from dans_pymodules import MyColors

__author__ = "Philip Weigel, Daniel Winklehner"
__doc__ = """A QT5 based GUI that allows loading particle data from 
various simulation codes and exporting them for various other simulation codes.
"""


class ParticleFile(object):
    """
    This object will contain a list of datasets and some attributes for easier handling.
    """

    # __slots__ = ("_filename", "_driver", "_debug", "_datasets", "_selected", "_index", "_parent")

    def __init__(self, filename, driver, index, load_type, debug=False, **kwargs):
        self._filename = filename
        self._driver = driver
        self._debug = debug
        self._datasets = []
        self._index = index
        self._load_type = load_type
        self._parent = kwargs.get("parent")
        self._c_i = kwargs.get("color_index")
        self._name = ""

        self._datasets_to_load = 1  # TODO: Multispecies

        self._prompt = None

    def add_dataset(self, dataset):
        self._datasets.append(dataset)

    def dataset_count(self):
        return len(self._datasets)

    def datasets(self):
        return self._datasets

    def filename(self):
        return self._filename

    def get_dataset(self, index):
        return self._datasets[index]

    def index(self):
        return self._index

    def load(self, load_index=0):

        # datasets_to_load = 1
        # for i in range(datasets_to_load):
        #     _ds = Dataset(indices=(self._index, i), debug=self._debug)
        #     _ds.load_from_file(filename=self._filename, driver=self._driver)
        #     _ds.assign_color(c_i)
        #     c_i += 1
        #     self._datasets.append(_ds)

        if load_index == self._datasets_to_load:
            # self._prompt = None
            if self._load_type == "add":
                self._parent.loaded_add_df(self)
            elif self._load_type == "new":
                self._parent.loaded_new_df(self)

            return 0

        elif load_index < self._datasets_to_load:

            self._prompt = SpeciesPrompt(parent=self)
            self._prompt.run()

            return 0

        else:

            return 1

    def species_callback(self, prompt, species, name):
        prompt.close()

        _ds = Dataset(indices=(self._index, len(self._datasets)), debug=self._debug, species=species)
        _ds.load_from_file(filename=self._filename, driver=self._driver, name=name)
        _ds.assign_color(self._c_i)

        self._c_i += 1
        self._datasets.append(_ds)

        self.load(load_index=len(self._datasets))

    def remove_dataset(self, selection):
        # if type(selection) is int:
        if isinstance(selection, int):
            del self._datasets[selection]
        # elif type(selection) is Dataset:
        elif isinstance(selection, Dataset):
            self._datasets.remove(selection)
        return 0

    def screen_size(self):
        return self._parent.screen_size()

    def set_dataset(self, index, dataset):
        self._datasets[index] = dataset

    def set_index(self, index):
        self._index = index


# TODO
class FieldFile(object):
    def __init__(self, filename, driver, index, debug=False):
        self._filename = filename
        self._driver = driver
        self._index = index
        self._debug = debug

    def filename(self):
        return self._filename

    def index(self):
        return self._index

    def load(self):
        pass

    def save(self):
        pass


class SpeciesPrompt(object):
    def __init__(self, parent):
        self._parent = parent

        self._window = QtGui.QMainWindow()
        self._windowGUI = Ui_SpeciesPrompt()
        self._windowGUI.setupUi(self._window)

        self._windowGUI.apply_button.clicked.connect(self.apply)

        for preset_name in sorted(presets.keys()):
            self._windowGUI.species_selection.addItem(preset_name)

    def apply(self):
        preset_name = self._windowGUI.species_selection.currentText()
        name = self._windowGUI.dataset_name.text()
        print("SpeciesPrompt.apply: name = {}".format(name))
        species = IonSpecies(preset_name, energy_mev=1.0)  # TODO: Energy? -PW
        self._parent.species_callback(self, species=species, name=name)

    def close(self):
        self._window.close()

        return 0

    def run(self):
        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._window.width())
        _y = 0.5 * (screen_size.height() - self._window.height())

        # --- Show the GUI --- #
        self._window.show()
        self._window.move(_x, _y)


class PyParticleProcessor(object):
    def __init__(self, debug=False):
        """
        Initialize the GUI
        """
        self._app = QtGui.QApplication([])  # Initialize the application
        self._app.setStyle('Fusion')  # Apply a GUI style

        self._debug = debug
        self._ci = 0  # A color index for datasets
        self._datafiles = []  # Container for holding the datasets
        self._datafile_buffer = []  # Buffer used to hold datafiles in memory while loading
        self._selections = []  # Temporary dataset selections
        self._last_path = ""  # Stores the last path from loading/saving files

        # --- Load the GUI from XML file and initialize connections --- #
        self._mainWindow = QtGui.QMainWindow()
        self._mainWindowGUI = Ui_MainWindow()
        self._mainWindowGUI.setupUi(self._mainWindow)

        # --- Get some widgets from the builder --- #
        self._tabs = self._mainWindowGUI.tabWidget
        self._tabs.currentChanged.connect(self.callback_tab_change)

        self._status_bar = self._mainWindowGUI.statusBar

        self._treewidget = self._mainWindowGUI.treeWidget
        self._treewidget.itemClicked.connect(self.treewidget_clicked)

        self._properties_select = self._mainWindowGUI.properties_combo
        self._properties_select.__setattr__("data_objects", [])
        self._properties_table = self._mainWindowGUI.properties_table
        self._properties_label = self._mainWindowGUI.properties_label
        self._properties_table.setHorizontalHeaderLabels(["Property", "Value"])
        self._properties_table.__setattr__("data", None)  # The currently selected data
        self._properties_label.setText("Properties")

        self._menubar = self._mainWindowGUI.menuBar
        self._menubar.setNativeMenuBar(False)  # This is needed to make the menu bar actually appear -PW

        # --- Connections --- #
        self._mainWindowGUI.actionQuit.triggered.connect(self.main_quit)
        self._mainWindowGUI.actionImport_New.triggered.connect(self.callback_load_new_ds)
        self._mainWindowGUI.actionImport_Add.triggered.connect(self.callback_load_add_ds)
        self._mainWindowGUI.actionRemove.triggered.connect(self.callback_delete_ds)
        self._mainWindowGUI.actionAnalyze.triggered.connect(self.callback_analyze)
        # self._mainWindowGUI.actionPlot.triggered.connect(self.callback_plot)
        self._mainWindowGUI.actionGenerate.triggered.connect(self.callback_generate)
        self._mainWindowGUI.actionExport_For.triggered.connect(self.callback_export)
        self._properties_table.cellChanged.connect(self.callback_table_item_changed)
        self._properties_select.currentIndexChanged.connect(self.callback_properties_select)

        # --- Populate the Tools Menu --- #
        self._tools_menu = self._mainWindowGUI.menuTools
        self._current_tool = None
        for tool_name, tool_object in sorted(tool_mapping.items()):
            action = QtWidgets.QAction(self._mainWindow)
            action.setText(tool_object[0])
            action.setObjectName(tool_name)
            # noinspection PyUnresolvedReferences
            action.triggered.connect(self.callback_tool_action)
            self._tools_menu.addAction(action)

        # --- Resize the columns in the treewidget --- #
        for i in range(self._treewidget.columnCount()):
            self._treewidget.resizeColumnToContents(i)

        # --- Initial population of the properties table --- #
        self._property_list = ["name", "steps", "particles", "mass", "energy", "charge", "current"]
        self._units_list = [None, None, None, "amu", "MeV", "e", "A"]
        self._properties_table.setRowCount(len(self._property_list))

        # --- Do some plot manager stuff --- #
        self._plot_manager = PlotManager(self)
        self._mainWindowGUI.actionRedraw.triggered.connect(self._plot_manager.redraw_plot)
        self._mainWindowGUI.actionNew_Plot.triggered.connect(self._plot_manager.new_plot)
        self._mainWindowGUI.actionModify_Plot.triggered.connect(self._plot_manager.modify_plot)
        self._mainWindowGUI.actionRemove_Plot.triggered.connect(self._plot_manager.remove_plot)

        # Store generator information
        self._gen = GeneratorGUI(self)
        self._gen_data = {}

        # Go through each property in the list
        for idx, item in enumerate(self._property_list):

            p_string = item.title()  # Create a string from the property name
            if self._units_list[idx] is not None:  # Check if the unit is not None
                p_string += " (" + self._units_list[idx] + ")"  # Add the unit to the property string

            p = QtGui.QTableWidgetItem(p_string)  # Create a new item with the property string
            p.setFlags(QtCore.Qt.NoItemFlags)  # Disable all item flags
            self._properties_table.setItem(idx, 0, p)  # Set the item to the corresponding row (first column)

            v = QtGui.QTableWidgetItem("")  # Create a blank item to be a value placeholder
            v.setFlags(QtCore.Qt.NoItemFlags)  # Disable all item flags
            self._properties_table.setItem(idx, 1, v)  # Set the item to the corresponding row (second column)

    def add_generated_dataset(self, data, settings):

        filename, driver = self.get_filename(action='save')  # Get a filename and driver
        df_i = len(self._datafiles)
        new_df = ParticleFile(filename=filename, driver=driver, index=df_i, load_type="add", parent=self)
        dataset = Dataset(indices=(df_i, 0), data=data,
                          species=IonSpecies(name=settings["species"], energy_mev=float(settings["energy"])))

        # We need a better way to do this -PW
        dataset.set_property("name", "Generated Dataset")
        # dataset.set_property("ion", IonSpecies(name=settings["species"], energy_mev=float(settings["energy"])))
        dataset.set_property("steps", 1)
        dataset.set_property("particles", int(settings["numpart"]))
        dataset.set_property("curstep", 0)
        dataset.assign_color(1)

        dataset.export_to_file(filename=filename, driver=driver)

        new_df.add_dataset(dataset=dataset)
        self._datafiles.append(new_df)

        top_level_item = QtGui.QTreeWidgetItem(self._treewidget)  # Create the top level item for the datafile

        top_level_item.setText(0, "")  # Selection box
        top_level_item.setText(1, "{}".format(df_i))  # Display the id of the datafile
        top_level_item.setText(2, self._datafiles[-1].filename())  # Display the filename

        top_level_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
        top_level_item.setCheckState(0, QtCore.Qt.Unchecked)  # Set the datafile to be unchecked by default

        self._properties_select.addItem("Datafile {}".format(df_i))  # Add an item to the property selection

        number_of_datasets = new_df.dataset_count()  # For now, assume there exists only one dataset

        for ds_i in range(number_of_datasets):  # Loop through each dataset

            child_item = QtGui.QTreeWidgetItem(top_level_item)  # Create a child item for the dataset
            child_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
            child_item.setCheckState(0, QtCore.Qt.Unchecked)  # Set the dataset to be unchecked by default
            self.add_tree_item(df_i, ds_i)  # Update the tree item with those indices

            # Add an item to the property selection
            self._properties_select.addItem("Datafile {}, Dataset {}".format(df_i, ds_i))

            # Conditional to check if there's only one dataset
            if number_of_datasets == 1:

                if not self._plot_manager.has_default_plot_settings():  # If the default plot settings aren't set...
                    self._plot_manager.default_plot_settings()  # Open the default plot settings GUI

                # If you want the dataset to automatically be unselected
                child_item.setCheckState(0, QtCore.Qt.Unchecked)

                # If you want the dataset to automatically be selected
                # child_item.setCheckState(0, QtCore.Qt.Checked)
                # self._selections.append("{}-{}".format(df_i, ds_i))

        top_level_item.setExpanded(True)  # Expand the tree widget

        for i in range(self._treewidget.columnCount()):  # Resize the columns of the tree
            self._treewidget.resizeColumnToContents(i)

    def add_to_properties_selection(self, datafile):
        self._properties_select.addItem("Datafile {}".format(datafile.index()))
        self._properties_select.data_objects.append(datafile)
        for index, dataset in enumerate(datafile.datasets()):
            self._properties_select.addItem("Datafile {}, Dataset {}".format(datafile.index(), index))
            self._properties_select.data_objects.append(dataset)

    def callback_about_program(self, menu_item):
        """
        :param menu_item:
        :return:
        """
        if self._debug:
            print("DEBUG: About Dialog called by {}".format(menu_item))

        return 0

    def callback_analyze(self):

        print("Not implemented yet!")

        for dataset in self._selections:
            for i in range(dataset.get_npart()):
                print(dataset.get("x")[i])
                print(dataset.get("y")[i])
                print(dataset.get("r")[i])
                print(dataset.get("px")[i])
                print(dataset.get("py")[i])

        return 0

    def callback_delete_ds(self):
        """
        Callback for Delete Dataset... button
        :return: 
        """

        if self._debug:
            print("DEBUG: delete_ds_callback was called")

        if len(self._selections) < 1:  # Check to make sure something was selected to remove
            msg = "You must select something to remove."
            print(msg)
            self.send_status(msg)

        redraw_flag = False  # Set a redraw flag to False
        root = self._treewidget.invisibleRootItem()  # Find the root item

        for selection in self._selections:
            redraw_flag = True
            if selection in self._properties_select.data_objects:
                index = self._properties_select.data_objects.index(selection)
                self._properties_select.removeItem(index)
                self._properties_select.data_objects.remove(selection)
                # if type(selection) is ParticleFile or type(selection) is FieldFile:
                if isinstance(selection, (ParticleFile, FieldFile)):
                    del self._datafiles[selection.index()]
                    item = self._treewidget.topLevelItem(selection.index())
                    (item.parent() or root).removeChild(item)
                    if len(self._properties_select.data_objects[index:]) > 0:
                        # while type(self._properties_select.data_objects[index]) is Dataset:
                        while isinstance(self._properties_select.data_objects[index], Dataset):
                            print(self._properties_select.data_objects[index].indices())
                            self._properties_select.removeItem(index)
                            del self._properties_select.data_objects[index]
                            if index == len(self._properties_select.data_objects):
                                break
                # elif type(selection) is Dataset:
                elif isinstance(selection, Dataset):
                    self._plot_manager.remove_dataset(selection)
                    parent_index = selection.indices()[0]
                    child_index = selection.indices()[1]
                    self._datafiles[parent_index].remove_dataset(selection)
                    item = self._treewidget.topLevelItem(parent_index).child(child_index)
                    (item.parent() or root).removeChild(item)

        self._selections = []

        if redraw_flag:  # If the redraw flag was set, redraw the plot
            self.refresh_data()
            self.clear_properties_table()
            self._plot_manager.redraw_plot()

        return 0

    def callback_export(self):

        if self._debug:
            "DEBUG: export_callback called"

        # TODO: This should make sure we're selecting a dataset vs. datafile
        if len(self._selections) == 0:  # Check to see if no datasets were selected
            msg = "No dataset was selected!"
            print(msg)
            self.send_status(msg)
            return 1
        elif len(self._selections) > 1:  # Check to see if too many datasets were selected
            msg = "You cannot select more than one dataset!"
            print(msg)
            self.send_status(msg)
            return 1

        filename, driver = self.get_filename(action='save')  # Get a filename and driver

        if (filename, driver) == (None, None):
            return 0

        selection = self._selections[0]
        selection.export_to_file(filename=filename, driver=driver)

        print("Export complete!")
        self.send_status("Export complete!")

        return 0

    def callback_load_add_ds(self, widget):
        """
        Callback for Add Dataset... button
        :return: 
        """

        if self._debug:
            print("DEBUG: load_add_ds_callback was called with widget {}".format(widget))

        filename, driver = self.get_filename(action="open")  # Get a filename and driver

        if filename is None:  # Return if no file was selected
            return 1

        self.send_status("Loading file with driver: {}".format(driver))

        # Create a new datafile with the supplied parameters
        new_df = ParticleFile(filename=filename,
                              driver=driver,
                              index=len(self._datafiles),
                              load_type="add",
                              debug=self._debug,
                              parent=self,
                              color_index=self._ci)

        new_df.load()

        self._datafile_buffer.append(new_df)

        return 0

    def loaded_add_df(self, new_df):
        # If the loading of the datafile is successful...

        self._datafiles.append(new_df)  # Add the datafile to the list
        self._datafile_buffer.remove(new_df)  # Remove the datafile from the buffer
        df_i = len(self._datafiles) - 1  # Since it's the latest datafile, it's the last index
        self._ci += new_df.dataset_count()  # TODO: Is this right?

        top_level_item = QtGui.QTreeWidgetItem(self._treewidget)  # Create the top level item for the datafile

        top_level_item.setText(0, "")  # Selection box
        top_level_item.setText(1, "{}".format(df_i))  # Display the id of the datafile
        top_level_item.setText(2, self._datafiles[-1].filename())  # Display the filename

        top_level_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
        top_level_item.setCheckState(0, QtCore.Qt.Unchecked)  # Set the datafile to be unchecked by default

        # self._properties_select.addItem("Datafile {}".format(df_i))  # Add an item to the property selection

        for ds_i in range(new_df.dataset_count()):  # Loop through each dataset

            child_item = QtGui.QTreeWidgetItem(top_level_item)  # Create a child item for the dataset
            child_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
            child_item.setCheckState(0, QtCore.Qt.Unchecked)  # Set the dataset to be unchecked by default
            self.add_tree_item(df_i, ds_i)  # Update the tree item with those indices

            # Add an item to the property selection
            # self._properties_select.addItem("Datafile {}, Dataset {}".format(df_i, ds_i))

            # Conditional to check if there's only one dataset
            if new_df.dataset_count() == 1:

                if not self._plot_manager.has_default_plot_settings():  # If the default plot settings aren't set...
                    self._plot_manager.default_plot_settings()  # Open the default plot settings GUI

                # If you want the dataset to automatically be unselected
                child_item.setCheckState(0, QtCore.Qt.Unchecked)

                # If you want the dataset to automatically be selected
                # child_item.setCheckState(0, QtCore.Qt.Checked)
                # self._selections.append("{}-{}".format(df_i, ds_i))

        self.add_to_properties_selection(new_df)

        top_level_item.setExpanded(True)  # Expand the tree widget

        for i in range(self._treewidget.columnCount()):  # Resize the columns of the tree
            self._treewidget.resizeColumnToContents(i)

        self.send_status("File loaded successfully!")

        return 0

    def callback_load_new_ds(self):
        """
        Callback for Load Dataset... button
        :return: 
        """

        if self._debug:
            print("DEBUG: load_new_ds_callback was called.")

        filename, driver = self.get_filename(action="open")  # Get a filename and driver

        if filename is None:  # Return if no file was selected
            return 1

        self.send_status("Loading file with driver: {}".format(driver))

        # Create a new datafile with the supplied parameters
        new_df = ParticleFile(filename=filename,
                              driver=driver,
                              index=0,
                              load_type="new",
                              debug=self._debug,
                              parent=self,
                              color_index=self._ci)

        new_df.load()

        self._datafile_buffer.append(new_df)

        return 0

    def loaded_new_df(self, new_df):
        # If the loading of the datafile is successful...

        self._datafiles = [new_df]  # Set the list of datafiles to just this one
        self._datafile_buffer.remove(new_df)  # Remove the datafile from the buffer
        df_i = 0  # Since it's the only datafile, it's the zeroth index
        self._ci += new_df.dataset_count()  # TODO: Is this right?

        top_level_item = QtGui.QTreeWidgetItem(self._treewidget)  # Create the top level item for the datafile

        top_level_item.setText(0, "")  # Selection box
        top_level_item.setText(1, "{}".format(df_i))  # Display the id of the datafile
        top_level_item.setText(2, self._datafiles[-1].filename())  # Display the filename

        top_level_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
        top_level_item.setCheckState(0, QtCore.Qt.Unchecked)  # Set the datafile to be unchecked by default

        # self._properties_select.addItem("Datafile {}".format(df_i))  # Add an item to the property selection

        number_of_datasets = 1  # For now, assume there exists only one dataset

        for ds_i in range(number_of_datasets):  # Loop through each dataset

            child_item = QtGui.QTreeWidgetItem(top_level_item)  # Create a child item for the dataset
            child_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
            child_item.setCheckState(0, QtCore.Qt.Unchecked)  # Set the dataset to be unchecked by default
            self.add_tree_item(df_i, ds_i)  # Update the tree item with those indices

            # Add an item to the property selection
            # self._properties_select.addItem("Datafile {}, Dataset {}".format(df_i, ds_i))

            # Conditional to check if there's only one dataset
            if number_of_datasets == 1:

                if not self._plot_manager.has_default_plot_settings():  # If the default plot settings aren't set...
                    self._plot_manager.default_plot_settings()  # Open the default plot settings GUI

                # If you want the dataset to automatically be unselected
                child_item.setCheckState(0, QtCore.Qt.Unchecked)

                # If you want the dataset to automatically be selected
                # child_item.setCheckState(0, QtCore.Qt.Checked)
                # self._selections.append("{}-{}".format(df_i, ds_i))

        self.add_to_properties_selection(new_df)

        top_level_item.setExpanded(True)  # Expand the tree widget

        for i in range(self._treewidget.columnCount()):  # Resize the columns of the tree
            self._treewidget.resizeColumnToContents(i)

        self.send_status("File loaded successfully!")

    # def callback_plot(self):
    #     # Called when the "Plot..." Button is pressed
    #
    #     if self._debug:
    #         "DEBUG: callback_plot called"
    #
    #     if self._tabs.currentIndex() == 0:  # Check to see if it's the default plot tab
    #         self._plot_manager.default_plot_settings(redraw=True)  # Open the default plot settings
    #     elif self._tabs.currentIndex() > 1:  # Check to see if it's after the text tab
    #         self._plot_manager.plot_settings()  # Open the plot settings
    #
    #     return 0

    def callback_generate(self):
        # Called when the "Generate..." button is pressed

        self._gen.run()
        # self._gen_data = self._gen.data

        # self.add_generated_data_set(self._gen.data)

    def callback_properties_select(self, index):

        # Get the text from the selected item in the properties selection
        txt = [item.rstrip(",") for item in self._properties_select.itemText(index).split()]

        # Format: "Datafile {}, Dataset {}" or "Datafile {}"
        if len(txt) == 4:  # If there are 4 items, it's a dataset
            df_i, ds_i = int(txt[1]), int(txt[3])  # Get the corresponding indices
            dataset = self.find_dataset(df_i, ds_i)  # Get the dataset
            self._properties_table.data = dataset  # Set the table's data property
            self.populate_properties_table(dataset)  # Populate the properties table with the dataset info

            return 0

        elif len(txt) == 2:  # If there are two items, it's a datafile
            df_i, ds_i = int(txt[1]), None  # Get the datafile index
            datafile = self._datafiles[df_i]  # Get the datafile object
            self._properties_table.data = datafile
            self.populate_properties_table(datafile)  # Populate the properties table with datafile info

            return 0

        elif index == -1:  # Check if the index is -1
            # This happens when there are no more datasets

            return 0

        else:  # This can only happen when something on the backend isn't working right

            print("Something went wrong!")

            return 1

    def callback_tab_change(self):

        current_index = self._tabs.currentIndex()
        current_plot_objects = self._plot_manager.get_plot_object(current_index)
        redraw = False

        for plot_object in current_plot_objects:
            for selection in self._selections:
                # if type(selection) is Dataset:
                if isinstance(selection, Dataset):
                    if selection not in plot_object.datasets():
                        plot_object.add_dataset(selection)
                        redraw = True

        if redraw:
            self._plot_manager.redraw_plot()

        return 0

    def callback_table_item_changed(self):
        v = self._properties_table.currentItem()  # Find the current item that was changed

        # Filter out some meaningless things that could call this function
        if v is None or v.text == "":
            return 0

        data = self._properties_table.data  # Get the datafile and dataset ids from the table

        # Filter out the condition that the program is just starting and populating the table
        if data is None:
            return 0

        # TODO: This might trigger a problem if a datafile is selected
        idx = self._properties_table.currentRow()  # Find the row of the value that was changed

        try:
            if idx != 0:
                value = float(v.text())  # Try to convert the input to a float
                v.setText(str(value))  # Reset the text of the table item to what was just set
                data.set_property(self._property_list[idx], value)  # Set the property of the dataset
            else:
                if self._debug:
                    print("Changing dataset name")
                value = v.text()
                data.set_property(self._property_list[idx], value)  # Set the name of the dataset
                self.refresh_data(properties=False)

            v.setForeground(QtGui.QBrush(QtGui.QColor("#FFFFFF")))  # If all this worked, then set the text color
            return 0

        except ValueError:
            # ds.set_property(self._property_list[idx], None)  # Set the dataset property to None
            v.setForeground(QtGui.QBrush(QtGui.QColor("#FF0000")))  # Set the text color to red
            return 1

    def callback_tool_action(self):

        sender = self._mainWindow.sender()
        name = sender.objectName()
        datasets = []

        for selection in self._selections:
            # if type(selection) is Dataset:
            if isinstance(selection, Dataset):
                datasets.append(selection)

        tool_object = tool_mapping[name][1]

        self._current_tool = tool_object(parent=self)
        self._current_tool.set_selections(datasets)

        if self._current_tool.redraw_on_exit():
            self._current_tool.set_plot_manager(self._plot_manager)

        if self._current_tool.check_requirements() == 0:
            self._current_tool.open_gui()

    def clear_properties_table(self):

        self._properties_table.setCurrentItem(None)  # Set the current item to None
        self._properties_table.data = None  # Clear the data property
        self._properties_label.setText("Properties")  # Set the label

        for idx in range(len(self._property_list)):  # Loop through each row
            v = QtGui.QTableWidgetItem("")  # Create a placeholder item
            v.setFlags(QtCore.Qt.NoItemFlags)  # Disable item flags
            self._properties_table.setItem(idx, 1, v)  # Add the item to the table

        return 0

    def find_dataset(self, datafile_id, dataset_id):
        return self._datafiles[datafile_id].get_dataset(dataset_id)  # Return the dataset object given the indices

    def get_default_graphics_views(self):
        # Return a tuple of the graphics views from the default plots tab
        default_gv = (self._mainWindowGUI.graphicsView_1,
                      self._mainWindowGUI.graphicsView_2,
                      self._mainWindowGUI.graphicsView_3,
                      self._mainWindowGUI.graphicsView_4)

        return default_gv

    def get_filename(self, action="open"):

        filename, filetype = "", ""

        # Format the filetypes selection
        first_flag1 = True
        filetypes_text = ""
        for key in sorted(driver_mapping.keys()):
            if len(driver_mapping[key]["extensions"]) > 0:
                if first_flag1:
                    filetypes_text += "{} Files (".format(key)
                    first_flag1 = False
                else:
                    filetypes_text += ";;{} Files (".format(key)
                first_flag2 = True
                for extension in driver_mapping[key]["extensions"]:
                    if first_flag2:
                        filetypes_text += "*{}".format(extension)
                        first_flag2 = False
                    else:
                        filetypes_text += " *{}".format(extension)
                filetypes_text += ")"

        # Create the file dialog options
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        if action == "open":  # For opening a file
            filename, filetype = QFileDialog.getOpenFileName(self._mainWindow,
                                                             caption="Import dataset...",
                                                             directory=self._last_path,
                                                             filter=filetypes_text,
                                                             options=options)
        elif action == "save":  # For saving a file
            filename, filetype = QFileDialog.getSaveFileName(self._mainWindow,
                                                             caption="Export dataset...",
                                                             directory=self._last_path,
                                                             filter=filetypes_text,
                                                             options=options)

        if filename == "" or filetype == "":
            filename, driver = None, None
            return filename, driver

        driver = filetype.split("Files")[0].strip()  # Get the driver from the filetype

        return filename, driver

    @staticmethod
    def get_selection(selection_string):

        if "-" in selection_string:  # If there's a hyphen, it's a dataset
            indices = selection_string.split("-")
            datafile_index, dataset_index = int(indices[0]), int(indices[1])  # Convert the strings to ints
            return datafile_index, dataset_index
        else:  # Or else it's a datafile
            datafile_index = int(selection_string)  # Convert the string into an int
            return datafile_index, None

    def initialize(self):
        """
        Do all remaining initializations
        :return: 0
        """

        if self._debug:
            print("DEBUG: Called initialize() function.")

        self._status_bar.showMessage("Program Initialized.")

        return 0

    def main_quit(self):
        """
        Shuts down the program (and threads) gracefully.
        :return:
        """

        if self._debug:
            print("DEBUG: Called main_quit")

        self._mainWindow.destroy()  # Close the window
        qApp.quit()  # Quit the application

        return 0

    def populate_properties_table(self, data_object):
        self.clear_properties_table()

        # if type(data_object) is ParticleFile:
        if isinstance(data_object, (ParticleFile, FieldFile)):  # If the object passed is a datafile...
            # df = data_object
            print("Datafile properties are not implemented yet!")
            return 1
        # elif type(data_object) is Dataset:
        elif isinstance(data_object, Dataset):  # If the object passed is a dataset...
            ds = data_object
            self._properties_table.data = ds
            # self._properties_label.setText("Properties (Datafile #{}, Dataset #{})".format(df_i, ds_i))
            for idx, item in enumerate(self._property_list):  # Enumerate through the properties list
                if ds.get_property(item) is not None:  # If the property is not None
                    v = QtWidgets.QTableWidgetItem(str(ds.get_property(item)))  # Set the value item
                    if ds.is_native_property(item):  # If it's a native property to the set, it's not editable
                        v.setFlags(QtCore.Qt.ItemIsEnabled)
                    else:  # If it is not a native property, it may be edited
                        v.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                else:  # IF the property wasn't found
                    v = QtWidgets.QTableWidgetItem("Property not found")  # Create a placeholder
                    v.setForeground(QtGui.QBrush(QtGui.QColor("#FF0000")))  # Set the text color to red
                    v.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)  # Make it editable
                self._properties_table.setItem(idx, 1, v)  # Put the item in the table

        return 0

    def refresh_data(self, properties=True):
        self._treewidget.clear()

        if properties:
            self._properties_select.clear()
            self._properties_select.data_objects = []

        for parent_index, datafile in enumerate(self._datafiles):
            datafile.set_index(parent_index)

            # --- Refresh Tree Widget for the Datafile --- #
            top_level_item = QtGui.QTreeWidgetItem(self._treewidget)

            top_level_item.setText(0, "")
            top_level_item.setText(1, "{}".format(parent_index))
            top_level_item.setText(2, datafile.filename())

            top_level_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            top_level_item.setCheckState(0, QtCore.Qt.Unchecked)

            for child_index, dataset in enumerate(datafile.datasets()):
                # --- Refresh Tree Widget for the Dataset --- #
                dataset.set_indices(parent_index, child_index)

                child_item = QtGui.QTreeWidgetItem(top_level_item)

                child_item.setText(0, "")  # Selection box
                child_item.setText(1, "{}-{}".format(parent_index, child_index))
                child_item.setText(2, "{}".format(dataset.get_name()))

                child_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
                child_item.setCheckState(0, QtCore.Qt.Unchecked)

                pass

            top_level_item.setExpanded(True)  # Expand the tree widget

            # --- Refresh the Properties Selection for the Datafile --- #
            if properties:
                self.add_to_properties_selection(datafile)

        for i in range(self._treewidget.columnCount()):  # Resize the columns of the tree
            self._treewidget.resizeColumnToContents(i)

    def run(self):
        """
        Run the GUI
        :return: 
        """
        self.initialize()

        # --- Calculate the positions to center the window --- #
        screen_size = self.screen_size()
        _x = 0.5 * (screen_size.width() - self._mainWindow.width())
        _y = 0.5 * (screen_size.height() - self._mainWindow.height())

        # --- Show the GUI --- #
        self._mainWindow.show()
        self._mainWindow.move(_x, _y)
        self._app.exec_()

        return 0

    def screen_size(self):
        return self._app.desktop().availableGeometry()  # Return the size of the screen

    def send_status(self, message):
        if isinstance(message, str):  # Make sure we're sending a string to the status bar
            self._status_bar.showMessage(message)
        else:
            print("Status message is not a string!")
            return 1

        return 0

    def tabs(self):
        return self._tabs  # Return the tab widget

    def treewidget_clicked(self, item, column):

        if self._debug:
            print("treewidget_data_changed callback called with item {} and column {}".format(item, column))

        if column == 0:  # If the first column was clicked
            checkstate = (item.checkState(0) == QtCore.Qt.Checked)  # Get a True or False value for selection
            index = self._treewidget.indexFromItem(item).row()  # Get the row index

            if item.parent() is None:  # If the item does not have a parent, it's a datafile
                selection = self._datafiles[index]
            else:  # If it does, it's a dataset
                parent_index = self._treewidget.indexFromItem(item.parent()).row()
                selection = self._datafiles[parent_index].get_dataset(index)

            if checkstate is True and selection not in self._selections:
                self._selections.append(selection)  # Add the string to the selections

                # if type(selection) is Dataset:
                if isinstance(selection, Dataset):
                    self._plot_manager.add_to_current_plot(selection)  # Add to plot
                    if not self._plot_manager.has_default_plot_settings():  # Check for default plot settings
                        self._plot_manager.default_plot_settings()  # Open the default plot settings
                    self._plot_manager.redraw_plot()  # Redraw the plot

            elif checkstate is False and selection in self._selections:
                self._selections.remove(selection)  # Remove the string from the selections

                # if type(selection) is Dataset:
                if isinstance(selection, Dataset):
                    self._plot_manager.remove_dataset(selection)  # Remove the dataset
                    self._plot_manager.redraw_plot()  # Redraw the plot

        return 0

    def add_tree_item(self, datafile_id, dataset_id):

        dataset = self._datafiles[datafile_id].get_dataset(dataset_id)  # Get the dataset object from the indices
        child_item = self._treewidget.topLevelItem(datafile_id).child(dataset_id)  # Create a child item

        child_item.setText(0, "")  # Selection box
        child_item.setText(1, "{}-{}".format(datafile_id, dataset_id))  # Set the object id
        # child_item.setText(2, "{}".format(dataset.get_ion().name()))  # Set the dataset name (for now, the ion name)
        child_item.setText(2, "{}".format(dataset.get_name()))  # Set the dataset name

        child_item.setFlags(child_item.flags() | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
