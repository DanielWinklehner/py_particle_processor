from py_particle_processor_qt.dataset import *
from py_particle_processor_qt.gui.main_window import *
from py_particle_processor_qt.plotting import *
from py_particle_processor_qt.tools import *
from PyQt5.QtWidgets import qApp, QFileDialog
# from dans_pymodules import MyColors
import time

__author__ = "Philip Weigel, Daniel Winklehner"
__doc__ = """A GTK+3 based GUI that allows loading particle data from 
various simulation codes and exporting them for various other simulation codes.
"""


class DataFile(object):
    """
    This object will contain a list of datasets and some attributes for easier handling.
    """
    __slots__ = ("_filename", "_driver", "_debug", "_datasets", "_selected", "_index")

    def __init__(self, filename, driver, index, debug=False):
        self._filename = filename
        self._driver = driver
        self._debug = debug
        self._datasets = []
        self._selected = []  # Probably temporary
        self._index = index

    def dataset_count(self):
        return len(self._datasets)

    def filename(self):
        return self._filename

    def get_dataset(self, index):
        return self._datasets[index]

    def get_selected(self):
        return [i for i, v in enumerate(self._selected) if v is True]

    def index(self):
        return self._index

    def load(self, c_i):
        number_of_datasets = 1
        for i in range(number_of_datasets):
            _ds = Dataset(indices=(self._index, i), debug=self._debug)
            _ds.load_from_file(filename=self._filename, driver=self._driver)
            _ds.assign_color(c_i)
            c_i += 1
            self._datasets.append(_ds)
        return 0

    def remove_dataset(self, index):
        del self._datasets[index]
        return 0

    def set_dataset(self, index, dataset):
        self._datasets[index] = dataset


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

        self._log_textbuffer = self._mainWindowGUI.textEdit_2

        self._treeview = self._mainWindowGUI.treeWidget
        self._treeview.itemClicked.connect(self.treeview_clicked)

        self._properties_select = self._mainWindowGUI.properties_combo
        self._properties_table = self._mainWindowGUI.properties_table
        self._properties_label = self._mainWindowGUI.properties_label
        self._properties_table.setHorizontalHeaderLabels(["Property", "Value"])
        self._properties_table.__setattr__("dfds", (None, None))  # Used to find the shown dataset
        self._properties_label.setText("Properties")

        self._menubar = self._mainWindowGUI.menuBar
        self._menubar.setNativeMenuBar(False)  # This is needed to make the menu bar actually appear -PW

        # --- Connections --- #
        self._mainWindowGUI.actionQuit.triggered.connect(self.main_quit)
        self._mainWindowGUI.actionImport_New.triggered.connect(self.callback_load_new_ds)
        self._mainWindowGUI.actionImport_Add.triggered.connect(self.callback_load_add_ds)
        self._mainWindowGUI.actionRemove.triggered.connect(self.callback_delete_ds)
        self._mainWindowGUI.actionAnalyze.triggered.connect(self.callback_analyze)
        self._mainWindowGUI.actionPlot.triggered.connect(self.callback_plot)
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

        # --- Resize the columns in the treeview --- #
        for i in range(self._treeview.columnCount()):
            self._treeview.resizeColumnToContents(i)

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

        # Go through each property in the list
        for idx, item in enumerate(self._property_list):

            p_string = item.title()  # Create a string from the property name
            if self._units_list[idx] is not None:  # Add the unit if it's not none
                p_string += " (" + self._units_list[idx] + ")"  # Add the unit to the property string

            p = QtGui.QTableWidgetItem(p_string)  # Create a new item with the property string
            p.setFlags(QtCore.Qt.NoItemFlags)  # Disable all item flags
            self._properties_table.setItem(idx, 0, p)  # Set the item to the corresponding row (first column)

            v = QtGui.QTableWidgetItem("")  # Create a blank item to be a value placeholder
            v.setFlags(QtCore.Qt.NoItemFlags)  # Disable all item flags
            self._properties_table.setItem(idx, 1, v)  # Set the item to the corresponding row (second column)

    def callback_about_program(self, menu_item):
        """
        :param menu_item:
        :return:
        """
        if self._debug:
            print("DEBUG: About Dialog called by {}".format(menu_item))

        return 0

    @staticmethod
    def callback_analyze():

        print("Not implemented yet!")

        # self._plot_manager.new_plot()
        # ds = self.get_selection(self._selections[0])
        # self._plot_manager.create_plot(self.find_dataset(ds[0], ds[1]))

        return 0

    def callback_table_item_changed(self):
        v = self._properties_table.currentItem()  # Find the current item that was changed

        # Filter out some meaningless things that could call this function
        if v is None or v.text == "":
            return 0

        df_i, ds_i = self._properties_table.dfds  # Get the datafile and dataset ids from the table

        # Filter out the condition that the program is just starting and populating the table
        if (df_i, ds_i) == (None, None):
            return 0

        # TODO: This might trigger a problem if a datafile is selected
        ds = self.find_dataset(df_i, ds_i)  # Get the corresponding dataset
        idx = self._properties_table.currentRow()  # Find the row of the value that was changed

        try:
            value = float(v.text())  # Try to convert the input to a float
            v.setText(str(value))  # Reset the text of the table item to what was just set

            ds.set_property(self._property_list[idx], value)  # Set the property of the dataset

            v.setForeground(QtGui.QBrush(QtGui.QColor("#FFFFFF")))  # If all this worked, then set the text color

            return 0

        except ValueError:
            # ds.set_property(self._property_list[idx], None)  # Set the dataset property to None
            v.setForeground(QtGui.QBrush(QtGui.QColor("#FF0000")))  # Set the text color to red

            return 1

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
        df_indices = []  # Initialize lists of items and indices for both datafiles and datasets
        df_items = []
        ds_indices = []
        ds_items = []
        root = self._treeview.invisibleRootItem()  # Find the root item

        for selection in self._selections:  # Go through each selection to delete
            redraw_flag = True  # If there was at least one selection, we will redraw
            df_i, ds_i = self.get_selection(selection)  # Get the datafile and dataset indices
            if ds_i is None:  # If there is no dataset index, then it's a datafile
                df_indices.append(df_i)  # Add the index to the list to remove
                df_items.append(self._treeview.topLevelItem(df_i))  # Add the item to the list to remove
            else:  # The other condition is that it is a dataset
                ds_indices.append((df_i, ds_i))  # Add both the datafile and dataset indices as a doublet
                ds_items.append(self._treeview.topLevelItem(df_i).child(ds_i))  # Add the dataset item to the list

        self._selections = []  # Clear the selections list

        # Remove the datasets first to avoid issues
        for df_i, ds_i in sorted(ds_indices, reverse=True):  # Sort backwards to prevent indexing errors
            count = 0
            for i in range(df_i):  # Find the number of preceding items in the property selection list
                count += self._datafiles[i].dataset_count() + 1
            self._properties_select.removeItem(count + ds_i + 1)  # Remove the dataset from the selection list
            self._plot_manager.remove_dataset(self.find_dataset(df_i, ds_i))  # Remove the dataset from the plots
            self._datafiles[df_i].remove_dataset(ds_i)  # Remove the dataset from the datafile

        for item in ds_items:  # Remove the dataset from its parent or root item
            (item.parent() or root).removeChild(item)

        # Remove the datafiles
        for df_i in sorted(df_indices, reverse=True):  # Sort backwards to prevent indexing errors
            count = 0
            for i in range(df_i):  # Find the number of preceding items in the property selection list
                count += self._datafiles[i].dataset_count() + 1
            self._properties_select.removeItem(count)  # Remove the datafile form the selection list
            del self._datafiles[df_i]  # Delete the datafile from the datafiles list

        for item in df_items:  # Remove the datafile from its parent or root item
            (item.parent() or root).removeChild(item)

        if redraw_flag:  # If the redraw flag was set, redraw the plot
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
        df_i, ds_i = self.get_selection(self._selections[0])  # Get the indices from the selection

        if (filename, driver) == (None, None):
            return 0

        # TODO: Modernize this statement
        self._datafiles[df_i].get_dataset(ds_i).export_to_file(filename=filename, driver=driver)

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
        new_df = DataFile(filename=filename, driver=driver, index=len(self._datafiles), debug=self._debug)

        if new_df.load(self._ci) == 0:  # If the loading of the datafile is successful...

            self._datafiles.append(new_df)  # Add the datafile to the list
            df_i = len(self._datafiles) - 1  # Since it's the latest datafile, it's the last index
            self._ci += new_df.dataset_count()  # TODO: Is this right?

            top_level_item = QtGui.QTreeWidgetItem(self._treeview)  # Create the top level item for the datafile

            top_level_item.setText(0, "")  # Selection box
            top_level_item.setText(1, "{}".format(df_i))  # Display the id of the datafile
            top_level_item.setText(2, self._datafiles[-1].filename())  # Display the filename

            top_level_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
            top_level_item.setCheckState(0, QtCore.Qt.Unchecked)  # Set the datafile to be unchecked by default

            self._properties_select.addItem("Datafile {}".format(df_i))  # Add an item to the property selection

            number_of_datasets = 1  # For now, assume there exists only one dataset

            for ds_i in range(number_of_datasets):  # Loop through each dataset

                child_item = QtGui.QTreeWidgetItem(top_level_item)  # Create a child item for the dataset
                child_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
                child_item.setCheckState(0, QtCore.Qt.Unchecked)  # Set the dataset to be unchecked by default
                self.update_tree_item(df_i, ds_i)  # Update the tree item with those indices

                # Add an item to the property selection
                self._properties_select.addItem("Datafile {}, Dataset {}".format(df_i, ds_i))

                # Conditional to check if there's only one dataset
                if number_of_datasets == 1:
                    ds = new_df.get_dataset(0)  # Get the first dataset from the datafile

                    if not self._plot_manager.has_default_plot_settings():  # If the default plot settings aren't set...
                        self._plot_manager.default_plot_settings()  # Open the default plot settings GUI

                    # If you want the dataset to automatically be unselected
                    child_item.setCheckState(0, QtCore.Qt.Unchecked)

                    # If you want the dataset to automatically be selected
                    # child_item.setCheckState(0, QtCore.Qt.Checked)
                    # self._selections.append("{}-{}".format(df_i, ds_i))

            top_level_item.setExpanded(True)  # Expand the tree widget

            for i in range(self._treeview.columnCount()):  # Resize the columns of the tree
                self._treeview.resizeColumnToContents(i)

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
        new_df = DataFile(filename=filename, driver=driver, index=0, debug=self._debug)

        if new_df.load(self._ci) == 0:  # If the loading of the datafile is successful...

            self._datafiles = [new_df]  # Set the list of datafiles to just this one
            df_i = 0  # Since it's the only datafile, it's the zeroth index
            self._ci += new_df.dataset_count()  # TODO: Is this right?

            top_level_item = QtGui.QTreeWidgetItem(self._treeview)  # Create the top level item for the datafile

            top_level_item.setText(0, "")  # Selection box
            top_level_item.setText(1, "{}".format(df_i))  # Display the id of the datafile
            top_level_item.setText(2, self._datafiles[-1].filename())  # Display the filename

            top_level_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
            top_level_item.setCheckState(0, QtCore.Qt.Unchecked)  # Set the datafile to be unchecked by default

            self._properties_select.addItem("Datafile {}".format(df_i))  # Add an item to the property selection

            number_of_datasets = 1  # For now, assume there exists only one dataset

            for ds_i in range(number_of_datasets):  # Loop through each dataset

                child_item = QtGui.QTreeWidgetItem(top_level_item)  # Create a child item for the dataset
                child_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
                child_item.setCheckState(0, QtCore.Qt.Unchecked)  # Set the dataset to be unchecked by default
                self.update_tree_item(df_i, ds_i)  # Update the tree item with those indices

                # Add an item to the property selection
                self._properties_select.addItem("Datafile {}, Dataset {}".format(df_i, ds_i))

                # Conditional to check if there's only one dataset
                if number_of_datasets == 1:
                    ds = new_df.get_dataset(0)  # Get the first dataset from the datafile

                    if not self._plot_manager.has_default_plot_settings():  # If the default plot settings aren't set...
                        self._plot_manager.default_plot_settings()  # Open the default plot settings GUI

                    # If you want the dataset to automatically be unselected
                    child_item.setCheckState(0, QtCore.Qt.Unchecked)

                    # If you want the dataset to automatically be selected
                    # child_item.setCheckState(0, QtCore.Qt.Checked)
                    # self._selections.append("{}-{}".format(df_i, ds_i))

            top_level_item.setExpanded(True)  # Expand the tree widget

            for i in range(self._treeview.columnCount()):  # Resize the columns of the tree
                self._treeview.resizeColumnToContents(i)

            self.send_status("File loaded successfully!")

        return 0

    def callback_plot(self):
        # Called when the "Plot..." Button is pressed

        if self._debug:
            "DEBUG: callback_plot called"

        if self._tabs.currentIndex() == 0:  # Check to see if it's the default plot tab
            self._plot_manager.default_plot_settings(redraw=True)  # Open the default plot settings
        elif self._tabs.currentIndex() > 1:  # Check to see if it's after the text tab
            self._plot_manager.plot_settings()  # Open the plot settings

        return 0

    def callback_properties_select(self, index):

        # Get the text from the selected item in the properties selection
        txt = [item.rstrip(",") for item in self._properties_select.itemText(index).split()]

        # Format: "Datafile {}, Dataset {}" or "Datafile {}"
        if len(txt) == 4:  # If there are 4 items, it's a dataset
            df_i, ds_i = int(txt[1]), int(txt[3])  # Get the corresponding indices
            dataset = self.find_dataset(df_i, ds_i)  # Get the dataset
            self._properties_table.dfds = (df_i, ds_i)  # Set the table's dfds property
            self.populate_properties_table(dataset)  # Populate the properties table with the dataset info

            return 0

        elif len(txt) == 2:  # If there are two items, it's a datafile
            df_i, ds_i = int(txt[1]), None  # Get the datafile index
            datafile = self._datafiles[df_i]  # Get the datafile object
            self._properties_table.dfds = (df_i, None)  # Set the table's dfds
            self.populate_properties_table(datafile)  # Populate the properties table with datafile info

            return 0

        elif index == -1:  # Check if the index is -1
            # This happens when there are no more datasets

            return 0

        else:  # This can only happen when something on the backend isn't working right

            print("Something went wrong!")

            return 1

    def callback_statusbar_changed(self, statusbar, context_id, text):
        """
        Callback that handles what happens when a message is pushed in the
        statusbar
        """

        if self._debug:
            print("Called statusbar_changed callback for statusbar {}, ID = {}".format(statusbar, context_id))

        _timestr = time.strftime("%d %b, %Y, %H:%M:%S: ", time.localtime())  # Get a string for the date and time

        self._log_textbuffer.insert(self._log_textbuffer.get_end_iter(), _timestr + text + "\n")  # Send to the buffer

        return 0

    def callback_tab_change(self):

        current_index = self._tabs.currentIndex()
        current_plot_objects = self._plot_manager.get_plot_object(current_index)
        redraw = False

        for plot_object in current_plot_objects:
            for selection_string in self._selections:
                df_i, ds_i = self.get_selection(selection_string)
                dataset = self.find_dataset(df_i, ds_i)
                if dataset not in plot_object.datasets():
                    plot_object.add_dataset(dataset)
                    redraw = True

        if redraw:
            self._plot_manager.redraw_plot()

        return 0

    def callback_tool_action(self):

        sender = self._mainWindow.sender()
        name = sender.objectName()
        datasets = []

        for selection_string in self._selections:
            df_i, ds_i = self.get_selection(selection_string)
            datasets.append(self.find_dataset(df_i, ds_i))

        tool_object = tool_mapping[name][1]

        self._current_tool = tool_object(parent=self)
        self._current_tool.set_selections(datasets)

        if self._current_tool.redraw_on_exit():
            self._current_tool.set_plot_manager(self._plot_manager)

        if self._current_tool.check_requirements() == 0:
            self._current_tool.open_gui()

    def clear_properties_table(self):

        self._properties_table.setCurrentItem(None)  # Set the current item to None
        self._properties_table.dfds = (None, None)  # Clear the dfds property
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

        if type(data_object) is DataFile:  # If the object passed is a datafile...
            # df = data_object
            print("Datafile properties are not implemented yet!")
            return 1
        elif type(data_object) is Dataset:  # If the object passed is a dataset...
            ds = data_object
            # self._properties_table.dfds = (df_i, ds_i)
            # self._properties_label.setText("Properties (Datafile #{}, Dataset #{})".format(df_i, ds_i))
            for idx, item in enumerate(self._property_list):  # Enumerate through the properties list
                if ds.get_property(item) is not None:  # If the property is not None
                    v = QtGui.QTableWidgetItem(str(ds.get_property(item)).title())  # Set the value item
                    if ds.is_native_property(item):  # If it's a native property to the set, it's not editable
                        v.setFlags(QtCore.Qt.ItemIsEnabled)
                    else:  # If it is not a native property, it may be edited
                        v.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                else:  # IF the property wasn't found
                    v = QtGui.QTableWidgetItem("Property not found")  # Create a placeholder
                    v.setForeground(QtGui.QBrush(QtGui.QColor("#FF0000")))  # Set the text color to red
                    v.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)  # Make it editable
                self._properties_table.setItem(idx, 1, v)  # Put the item in the table

        return 0

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
        if type(message) is str:  # Make sure we're sending a string to the status bar
            self._status_bar.showMessage(message)
        else:
            print("Status message is not a string!")
            return 1

        return 0

    def tabs(self):
        return self._tabs  # Return the tab widget

    def treeview_clicked(self, item, column):

        if self._debug:
            print("treeview_data_changed callback called with item {} and column {}".format(item, column))

        if column == 0:  # If the first column was clicked
            checkstate = (item.checkState(0) == QtCore.Qt.Checked)  # Get a True or False value for selection
            index = self._treeview.indexFromItem(item).row()  # Get the row index

            if item.parent() is None:  # If the item does not have a parent, it's a datafile
                selection_string = "{}".format(index)
            else:  # If it does, it's a dataset
                parent_index = self._treeview.indexFromItem(item.parent()).row()
                selection_string = "{}-{}".format(parent_index, index)

            if checkstate is True and selection_string not in self._selections:
                self._selections.append(selection_string)  # Add the string to the selections
                df_i, ds_i = self.get_selection(selection_string)  # Get the indices from the string

                if ds_i is not None:  # If it is a dataset...
                    self._plot_manager.add_to_current_plot(self.find_dataset(df_i, ds_i))  # Add to plot
                    if not self._plot_manager.has_default_plot_settings():  # Check for default plot settings
                        self._plot_manager.default_plot_settings()  # Open the default plot settings
                    self._plot_manager.redraw_plot()  # Redraw the plot

            elif checkstate is False and selection_string in self._selections:
                df_i, ds_i = self.get_selection(selection_string)  # Get the indices from the string
                self._selections.remove(selection_string)  # Remove the string from the selections

                if ds_i is not None:  # If it is a dataset...
                    self._plot_manager.remove_dataset(self.find_dataset(df_i, ds_i))  # Remove the dataet
                    self._plot_manager.redraw_plot()  # Redraw the plot

        return 0

    def update_tree_item(self, datafile_id, dataset_id):

        dataset = self._datafiles[datafile_id].get_dataset(dataset_id)  # Get the dataset object from the indices
        child_item = self._treeview.topLevelItem(datafile_id).child(dataset_id)  # Create a child item

        child_item.setText(0, "")  # Selection box
        child_item.setText(1, "{}-{}".format(datafile_id, dataset_id))  # Set the object id
        child_item.setText(2, "{}".format(dataset.get_ion().name()))  # Set the dataset name (for now, the ion name)

        child_item.setFlags(child_item.flags() | QtCore.Qt.ItemIsUserCheckable)  # Set item flags
