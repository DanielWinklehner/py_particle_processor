from py_particle_processor_qt.dataset import *
from py_particle_processor_qt.gui.main_window import *
from py_particle_processor_qt.plotting import *
from PyQt5.QtWidgets import qApp, QFileDialog
# from dans_pymodules import MyColors
import time


__author__ = "Philip Weigel, Daniel Winklehner"
__doc__ = """A GTK+3 based GUI that allows loading particle data from 
various simulation codes and exporting them for various other simulation codes.
"""

# Initialize some global constants
amu = const.value("atomic mass constant energy equivalent in MeV")
echarge = const.value("elementary charge")
clight = const.value("speed of light in vacuum")


class DataFile(object):
    """
    This object will contain a list of datasets and some attributes for easier handling.
    """
    __slots__ = ("_filename", "_driver", "_debug", "_datasets", "_selected")

    def __init__(self, filename, driver, debug=False):
        self._filename = filename
        self._driver = driver
        self._debug = debug
        self._datasets = []
        self._selected = []  # Probably temporary

    def dataset_count(self):
        return len(self._datasets)

    def filename(self):
        return self._filename

    def get_dataset(self, index):
        return self._datasets[index]

    def get_selected(self):
        return [i for i, v in enumerate(self._selected) if v is True]

    def load(self, c_i):

        number_of_datasets = 1
        for i in range(number_of_datasets):
            _ds = Dataset(debug=self._debug)
            _ds.load_from_file(filename=self._filename, driver=self._driver)
            _ds.assign_color(c_i)
            c_i += 1
            self._datasets.append(_ds)
        return 0

    def remove_dataset(self, index):
        del self._datasets[index]
        return 0


class PyParticleProcessor(object):

    def __init__(self, debug=False):
        """
        Initialize the GUI
        """
        self._app = QtGui.QApplication([])  # Initialize the application
        self._app.setStyle('Fusion')

        self._debug = debug
        self._ci = 0  # A color index for datasets
        self._datafiles = []  # Container for holding the datasets
        self._selections = []  # Temporary dataset selections
        self._last_path = ""  # Stores the last path from loading/saving files
        self._children = []

        # --- Load the GUI from XML file and initialize connections --- #
        self._mainWindow = QtGui.QMainWindow()
        self._mainWindowGUI = Ui_MainWindow()
        self._mainWindowGUI.setupUi(self._mainWindow)

        # --- Get some widgets from the builder --- #
        self._tabs = self._mainWindowGUI.tabWidget

        self._status_bar = self._mainWindowGUI.statusBar

        self._log_textbuffer = self._mainWindowGUI.textEdit_2

        self._treeview = self._mainWindowGUI.treeWidget

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
        self._properties_table.cellChanged.connect(self.callback_cell_changed)
        self._properties_select.currentIndexChanged.connect(self.callback_properties_select)
        self._treeview.itemClicked.connect(self.treeview_clicked)

        # --- Resize the columns in the treeview --- #
        for i in range(self._treeview.columnCount()):
            self._treeview.resizeColumnToContents(i)

        # --- Initial population of the properties table --- #
        self._property_list = ["name", "steps", "particles", "mass", "energy", "charge", "current"]
        self._units_list = [None, None, None, "amu", "MeV", "e", "A"]
        self._properties_table.setRowCount(len(self._property_list))

        # --- Do some plot manager stuff --- #
        self._plot_manager = PlotManager(self)
        self._mainWindowGUI.actionNew_Plot.triggered.connect(self._plot_manager.new_plot)
        self._mainWindowGUI.actionModify_Plot.triggered.connect(self._plot_manager.modify_plot)
        self._mainWindowGUI.actionRemove_Plot.triggered.connect(self._plot_manager.remove_plot)

        for idx, item in enumerate(self._property_list):

            p_string = item.title()
            if self._units_list[idx] is not None:  # Add the unit if it's not none
                p_string += " (" + self._units_list[idx] + ")"

            p = QtGui.QTableWidgetItem(p_string)
            p.setFlags(QtCore.Qt.NoItemFlags)
            self._properties_table.setItem(idx, 0, p)

            v = QtGui.QTableWidgetItem("")
            v.setFlags(QtCore.Qt.NoItemFlags)
            self._properties_table.setItem(idx, 1, v)

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

    def callback_cell_changed(self):
        # Used for checking changed values in the property table
        v = self._properties_table.currentItem()

        # Filter out some of the other calls
        if v is None or v.text == "":
            return 0

        df_i, ds_i = self._properties_table.dfds

        if (df_i, ds_i) == (None, None):
            return 0

        ds = self.find_dataset(df_i, ds_i)
        idx = self._properties_table.currentRow()

        try:
            value = float(v.text())
            v.setText(str(value))  # Just a precaution

            # We also need to update the particle's properties
            ds.set_property(self._property_list[idx], value)

            # Only change the text color if it worked
            v.setForeground(QtGui.QBrush(QtGui.QColor("#FFFFFF")))

            return 0

        except ValueError:
            ds.set_property(self._property_list[idx], None)
            v.setForeground(QtGui.QBrush(QtGui.QColor("#FF0000")))

            return 1

    def callback_delete_ds(self):
        """
        Callback for Delete Dataset... button
        :return: 
        """

        if self._debug:
            print("DEBUG: delete_ds_callback was called")

        if len(self._selections) < 1:
            msg = "You must select something to remove."
            print(msg)
            self.send_status(msg)

        redraw_flag = False
        df_indices = []
        df_items = []
        ds_indices = []
        ds_items = []
        root = self._treeview.invisibleRootItem()

        for selection in self._selections:
            redraw_flag = True
            df_i, ds_i = self.get_selection(selection)
            if ds_i is None:
                df_indices.append(df_i)
                df_items.append(self._treeview.topLevelItem(df_i))
            else:
                ds_indices.append((df_i, ds_i))
                ds_items.append(self._treeview.topLevelItem(df_i).child(ds_i))

        self._selections = []

        # Remove the datasets first to avoid problems
        for df_i, ds_i in sorted(ds_indices, reverse=True):
            i, count = 0, 0
            while i < df_i:
                count += self._datafiles[i].dataset_count() + 1
                i += 1
            self._properties_select.removeItem(count + ds_i + 1)
            self._plot_manager.remove_dataset(self.find_dataset(df_i, ds_i))
            self._datafiles[df_i].remove_dataset(ds_i)

        for item in ds_items:
            (item.parent() or root).removeChild(item)

        # Then remove the datafiles
        for df_i in sorted(df_indices, reverse=True):
            i, count = 0, 0
            while i < df_i:
                count += self._datafiles[i].dataset_count() + 1
                i += 1
            self._properties_select.removeItem(count)
            del self._datafiles[df_i]

        for item in df_items:
            (item.parent() or root).removeChild(item)

        if redraw_flag:
            self.clear_plots()

        return 0

    def callback_export(self):

        if self._debug:
            "DEBUG: export_callback called"

        if len(self._selections) == 0:
            msg = "No dataset was selected!"
            print(msg)
            self.send_status(msg)
            return 1
        elif len(self._selections) > 1:
            msg = "You cannot select more than one dataset!"
            print(msg)
            self.send_status(msg)
            return 1

        filename, driver = self.get_filename(action='save')
        df_i, ds_i = self.get_selection(self._selections[0])

        self._datafiles[df_i].get_dataset(ds_i).export_to_file(filename=filename, driver=driver)

        print("Export complete!")
        self.send_status("Export complete!")

    def callback_load_add_ds(self, widget):
        """
        Callback for Add Dataset... button
        :return: 
        """

        if self._debug:
            print("DEBUG: load_add_ds_callback was called with widget {}".format(widget))

        filename, driver = self.get_filename(action="open")

        if filename is None:
            return 1

        self.send_status("Loading file with driver: {}".format(driver))

        new_df = DataFile(filename=filename, driver=driver, debug=self._debug)

        if new_df.load(self._ci) == 0:

            self._datafiles.append(new_df)
            df_i = len(self._datafiles) - 1  # Load add, so it's the last id
            self._ci += new_df.dataset_count()

            # Create the top level item for the file
            top_level_item = QtGui.QTreeWidgetItem(self._treeview)

            top_level_item.setText(0, "")  # Selection
            top_level_item.setText(1, "{}".format(df_i))
            top_level_item.setText(2, self._datafiles[-1].filename())  # Name

            top_level_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            top_level_item.setCheckState(0, QtCore.Qt.Unchecked)

            self._properties_select.addItem("Datafile {}".format(df_i))

            number_of_datasets = 1

            for ds_i in range(number_of_datasets):

                child_item = QtGui.QTreeWidgetItem(top_level_item)
                child_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
                child_item.setCheckState(0, QtCore.Qt.Unchecked)
                self.update_tree_item(df_i, ds_i)

                self._properties_select.addItem("Datafile {}, Dataset {}".format(df_i, ds_i))

                if number_of_datasets == 1:
                    ds = new_df.get_dataset(0)

                    if not self._plot_manager.has_default_settings():
                        self._plot_manager.default_plot_settings()

                    # If you want the dataset to automatically be unselected
                    child_item.setCheckState(0, QtCore.Qt.Unchecked)

                    # If you want the dataset to automatically be selected
                    # child_item.setCheckState(0, QtCore.Qt.Checked)
                    # self._selections.append("{}-{}".format(df_i, ds_i))

            top_level_item.setExpanded(True)

            for i in range(self._treeview.columnCount()):
                self._treeview.resizeColumnToContents(i)

            self.send_status("File loaded successfully!")

        return 0

    def callback_load_new_ds(self):
        """
        Callback for Load Dataset... button
        :return: 
        """

        if self._debug:
            print("DEBUG: load_new_ds_callback was called")

        filename, driver = self.get_filename(action='open')

        if filename is None:
            return 1

        self.send_status("Loading file with driver: {}...".format(driver))

        new_df = DataFile(filename=filename, driver=driver, debug=self._debug)

        if new_df.load(self._ci) == 0:

            self._datafiles = [new_df]
            df_i = 0  # Load new, so the id is zero
            self._ci += new_df.dataset_count()

            self._treeview.clear()

            # Create the top level item for the file
            top_level_item = QtGui.QTreeWidgetItem(self._treeview)

            top_level_item.setText(0, "")  # Selection
            top_level_item.setText(1, "{}".format(df_i))
            top_level_item.setText(2, self._datafiles[0].filename())  # Name

            top_level_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            top_level_item.setCheckState(0, QtCore.Qt.Unchecked)

            self._properties_select.addItem("Datafile {}".format(df_i))

            number_of_datasets = 1

            for ds_i in range(number_of_datasets):

                child_item = QtGui.QTreeWidgetItem(top_level_item)
                child_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
                child_item.setCheckState(0, QtCore.Qt.Unchecked)
                self.update_tree_item(df_i, ds_i)
                self._properties_select.addItem("Datafile {}, Dataset {}".format(df_i, ds_i))

                if number_of_datasets == 1:
                    ds = new_df.get_dataset(0)

                    self._plot_manager.default_plot_settings()

                    # If you want the dataset to automatically be unselected
                    child_item.setCheckState(0, QtCore.Qt.Unchecked)

                    # If you want the dataset to automatically be selected
                    # child_item.setCheckState(0, QtCore.Qt.Checked)
                    # self._selections.append("{}-{}".format(df_i, ds_i))

            top_level_item.setExpanded(True)

            for i in range(self._treeview.columnCount()):
                self._treeview.resizeColumnToContents(i)

            self.send_status("File loaded successfully!")

        return 0

    def callback_notebook_page_changed(self, notebook, page, page_num):
        """
        Callback for when user switches to a different notebook page in the main notebook.
        :param notebook: a pointer to the gtk notebook object
        :param page: a pointer to the top level child of the page
        :param page_num: page number starting at 0
        :return:
        """

        if self._debug:
            print("DEBUG: Notebook {} changed page to {} (page_num = {})".format(notebook,
                                                                                 page,
                                                                                 page_num))
        return 0

    def callback_plot(self):

        if self._debug:
            "DEBUG: callback_plot called"

        if len(self._selections) == 0:
            msg = "No dataset was selected!"
            print(msg)
            self.send_status(msg)
            return 1
        elif len(self._selections) > 1:
            msg = "Showing properties of the last selected dataset."
            print(msg)
            self.send_status(msg)

        if self._tabs.currentIndex() == 0:
            self._plot_manager.default_plot_settings(redraw=True)

        # TODO: Plot settings for custom plots
        return 0

    def callback_properties_select(self, index):
        txt = [item.rstrip(",") for item in self._properties_select.itemText(index).split()]

        if len(txt) == 4:
            df_i, ds_i = int(txt[1]), int(txt[3])
            dataset = self.find_dataset(df_i, ds_i)
            self._properties_table.dfds = (df_i, ds_i)
            self.populate_properties_table(dataset)
        elif len(txt) == 2:
            df_i, ds_i = int(txt[1]), None
            datafile = self._datafiles[df_i]
            self._properties_table.dfds = (df_i, None)
            self.populate_properties_table(datafile)
        elif index == -1:
            # This happens when there are no more datasets (index is -1)
            return 0

        else:
            # Something probably went wrong...
            print("Something went wrong!")
            return 1

        return 0

    def callback_statusbar_changed(self, statusbar, context_id, text):
        """
        Callback that handles what happens when a message is pushed in the
        statusbar
        """

        if self._debug:
            print("Called statusbar_changed callback for statusbar {}, ID = {}".format(statusbar, context_id))

        _timestr = time.strftime("%d %b, %Y, %H:%M:%S: ", time.localtime())

        self._log_textbuffer.insert(self._log_textbuffer.get_end_iter(), _timestr + text + "\n")

        return 0

    def cell_toggled(self, widget, path, model, mode):
        """
        Callback function for toggling one of the checkboxes in the species
        TreeView. Updates the View and refreshes the plots...
        """
        if self._debug:
            print("DEBUG: cell_toggled was called with widget {} and mode {}".format(widget, mode))

        model[path][0] = not model[path][0]

        return 0

    def clear_plots(self):
        """
        Clear the plot windows
        :return: 
        """

        if self._debug:
            print("DEBUG: clear_plots called")

        for data_item in self._mainWindowGUI.graphicsView_1.listDataItems():
            self._mainWindowGUI.graphicsView_1.removeItem(data_item)
        for data_item in self._mainWindowGUI.graphicsView_2.listDataItems():
            self._mainWindowGUI.graphicsView_2.removeItem(data_item)
        for data_item in self._mainWindowGUI.graphicsView_3.listDataItems():
            self._mainWindowGUI.graphicsView_3.removeItem(data_item)

        # Using the removeItem(data_item) method does not work properly, this is a workaround -PW
        self._mainWindowGUI.graphicsView_4.items = []
        self._mainWindowGUI.graphicsView_4.update()

        self.send_status("Views cleared!")

        return 0

    def clear_properties_table(self):

        self._properties_table.setCurrentItem(None)
        self._properties_table.dfds = (None, None)
        self._properties_label.setText("Properties")

        for idx in range(len(self._property_list)):
            v = QtGui.QTableWidgetItem("")
            v.setFlags(QtCore.Qt.NoItemFlags)
            self._properties_table.setItem(idx, 1, v)

        return 0

    def find_dataset(self, datafile_id, dataset_id):
        return self._datafiles[datafile_id].get_dataset(dataset_id)

    def get_default_graphics_views(self):

        default_gv = (self._mainWindowGUI.graphicsView_1,
                      self._mainWindowGUI.graphicsView_2,
                      self._mainWindowGUI.graphicsView_3,
                      self._mainWindowGUI.graphicsView_4)

        return default_gv

    def get_filename(self, action="open"):

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

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        if action == "open":
            filename, filetype = QFileDialog.getOpenFileName(self._mainWindow,
                                                             caption="Import dataset...",
                                                             directory=self._last_path,
                                                             filter=filetypes_text,
                                                             options=options)
        elif action == "save":
            filename, filetype = QFileDialog.getSaveFileName(self._mainWindow,
                                                             caption="Export dataset...",
                                                             directory=self._last_path,
                                                             filter=filetypes_text,
                                                             options=options)
        else:
            filename, filetype = "", None

        if filename == "":
            return None, None

        driver = filetype.split("Files")[0].strip()

        return filename, driver

    @staticmethod
    def get_selection(selection_string):
        if "-" in selection_string:  # "#(item)"
            indices = selection_string.split("-")
            datafile_index, dataset_index = int(indices[0]), int(indices[1])
            return datafile_index, dataset_index
        else:
            datafile_index = int(selection_string)
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

        self._mainWindow.destroy()
        qApp.quit()

        return 0

    def populate_properties_table(self, object):
        self.clear_properties_table()

        if type(object) is DataFile:
            df = object
            # TODO: Datafile properties -PW
            print("Datafile properties are not implemented yet!")
            return 1
        elif type(object) is Dataset:
            ds = object
            # self._properties_table.dfds = (df_i, ds_i)
            # self._properties_label.setText("Properties (Datafile #{}, Dataset #{})".format(df_i, ds_i))
            for idx, item in enumerate(self._property_list):
                if ds.get_property(item) is not None:
                    v = QtGui.QTableWidgetItem(str(ds.get_property(item)).title())
                    if ds.is_native_property(item):
                        v.setFlags(QtCore.Qt.ItemIsEnabled)
                    else:
                        v.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                    self._properties_table.setItem(idx, 1, v)
                else:
                    v = QtGui.QTableWidgetItem("Property not found")
                    v.setForeground(QtGui.QBrush(QtGui.QColor("#FF0000")))
                    v.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                    self._properties_table.setItem(idx, 1, v)

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
        return self._app.desktop().availableGeometry()

    def send_status(self, message):
        if type(message) is str:
            self._status_bar.showMessage(message)
        else:
            print("Status message is not a string!")
            return 1

        return 0

    def tabs(self):
        return self._tabs

    def treeview_clicked(self, item, column):

        if self._debug:
            print("treeview_data_changed callback called with item {} and column {}".format(item, column))

        if column == 0:
            checkstate = (item.checkState(0) == QtCore.Qt.Checked)
            index = self._treeview.indexFromItem(item).row()

            if item.parent() is None:
                selection_string = "{}".format(index)
            else:
                parent_index = self._treeview.indexFromItem(item.parent()).row()
                selection_string = "{}-{}".format(parent_index, index)

            if checkstate is True and selection_string not in self._selections:
                self._selections.append(selection_string)
                df_i, ds_i = self.get_selection(selection_string)

                if ds_i is not None:  # If it is a dataset, plot
                    self._plot_manager.add_to_current_plot(self.find_dataset(df_i, ds_i))
                    if not self._plot_manager.has_default_settings():
                        self._plot_manager.default_plot_settings()
                    self._plot_manager.redraw_plot()

            elif checkstate is False and selection_string in self._selections:
                df_i, ds_i = self.get_selection(selection_string)
                self._selections.remove(selection_string)

                if ds_i is not None:
                    self._plot_manager.remove_dataset(self.find_dataset(df_i, ds_i))
                    self._plot_manager.redraw_plot()

        return 0

    def update_tree_item(self, datafile_id, dataset_id):

        dataset = self._datafiles[datafile_id].get_dataset(dataset_id)
        child_item = self._treeview.topLevelItem(datafile_id).child(dataset_id)

        child_item.setText(0, "")
        child_item.setText(1, "{}-{}".format(datafile_id, dataset_id))
        child_item.setText(2, "{}".format(dataset.get_ion().name()))

        child_item.setFlags(child_item.flags() | QtCore.Qt.ItemIsUserCheckable)
