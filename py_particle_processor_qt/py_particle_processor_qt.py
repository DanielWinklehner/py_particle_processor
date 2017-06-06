from py_particle_processor_qt.dataset import *
from py_particle_processor_qt.mainwindow import *
from py_particle_processor_qt.properties import *
from dans_pymodules import MyColors
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import qApp, QFileDialog
import time
import pyqtgraph as pg
import numpy as np

__author__ = "Philip Weigel, Daniel Winklehner"
__doc__ = """A GTK+3 based GUI that allows loading particle data from 
various simulation codes and exporting them for various other simulation codes.
"""

# Initialize some global constants
amu = const.value("atomic mass constant energy equivalent in MeV")
echarge = const.value("elementary charge")
clight = const.value("speed of light in vacuum")

# TODO: Tree structure for multiple datasets from one file -PW


class DataFile(object):
    """
    This object will contain a list of datasets and some attributes for easier handling.
    """
    def __init__(self, filename, driver, debug=False):
        self._filename = filename
        self._driver = driver
        self._debug = debug
        self._datasets = []
        self._selected = []  # Probably temporary

    @property
    def filename(self):
        return self._filename

    def get_dataset(self, index):
        return self._datasets[index]

    def get_selected(self):
        return [i for i, v in enumerate(self._selected) if v is True]

    def load(self):
        # TODO: How to get each dataset from one file? For now, it's just one.
        number_of_datasets = 1
        for i in range(number_of_datasets):
            _ds = Dataset(debug=self._debug)
            _ds.load_from_file(filename=self._filename, driver=self._driver)
            # TODO: Missing parameters?
            self._datasets.append(_ds)
        return 0


class PyParticleProcessor(object):

    def __init__(self, debug=False):
        """
        Initialize the GUI
        """
        self._app = QtGui.QApplication([])  # Initialize the application
        self._app.setStyle('Fusion')

        self._debug = debug
        self._colors = MyColors()
        self._datafiles = []  # Container for holding the datasets
        self._selections = []  # Temporary dataset selections
        self._last_path = ""  # TODO: Not working yet -PW
        self._pm = None  # Used to keep the property manager in scope

        # --- Load the GUI from XML file and initialize connections --- #
        self._mainWindow = QtGui.QMainWindow()
        self._mainWindowGUI = Ui_MainWindow()
        self._mainWindowGUI.setupUi(self._mainWindow)

        # --- Get some widgets from the builder --- #
        self._status_bar = self._mainWindowGUI.statusBar
        self._log_textbuffer = self._mainWindowGUI.textEdit_2
        self._treeview = self._mainWindowGUI.treeWidget
        self._menubar = self._mainWindowGUI.menuBar
        self._menubar.setNativeMenuBar(False)  # This is needed to make the menu bar actually appear -PW

        # --- Connections --- #
        self._mainWindowGUI.actionQuit.triggered.connect(self.main_quit)
        self._mainWindowGUI.actionImport_New.triggered.connect(self.callback_load_new_ds)
        self._mainWindowGUI.actionImport_Add.triggered.connect(self.callback_load_add_ds)
        self._mainWindowGUI.actionUnload_Selected.triggered.connect(self.callback_delete_ds)
        self._mainWindowGUI.actionProperties.triggered.connect(self.callback_properties)
        self._mainWindowGUI.actionAnalyze.triggered.connect(self.callback_analyze)
        self._mainWindowGUI.actionPlot.triggered.connect(self.callback_plot)
        self._mainWindowGUI.actionExport_For.triggered.connect(self.callback_export)
        self._treeview.itemClicked.connect(self.treeview_clicked)

        # --- Resize the columns in the treeview --- #
        for i in range(self._treeview.columnCount()):
            self._treeview.resizeColumnToContents(i)

    def apply_plot_settings(self, datafile_id, dataset_id, plot_settings):

        # TODO: Fix the changing step number for datasets -PW

        self._datafiles[datafile_id].get_dataset(dataset_id).set_plot_settings(plot_settings)

        return 0

    def callback_about_program(self, menu_item):
        """
        :param menu_item:
        :return:
        """
        if self._debug:
            print("DEBUG: About Dialog called by {}".format(menu_item))

        return 0

    @staticmethod  # For now... -PW
    def callback_analyze():
        # TODO: Create a new analysis tool for beam parameters -PW
        print("Not implemented yet!")

        return 0

    def callback_delete_ds(self):
        """
        Callback for Delete Dataset... button
        :return: 
        """

        # TODO: Handle removing a top level item vs. not a top level item
        # TODO: This probably doesn't work right now -PW

        if self._debug:
            print("DEBUG: delete_ds_callback was called")

        redraw_flag = False
        row_indices = range(self._treeview.topLevelItemCount())
        indices_to_remove = []
        items_to_remove = []
        root = self._treeview.invisibleRootItem()
        for i in row_indices:
            item = self._treeview.topLevelItem(i)
            if item.checkState(0) == QtCore.Qt.Checked:
                redraw_flag = True
                indices_to_remove.append(i)
                items_to_remove.append(item)

        for j in indices_to_remove:
            del self._datafiles[j]
            del self._selections[j]

        for item in items_to_remove:
            (item.parent() or root).removeChild(item)

        if redraw_flag:
            self.clear_plots()

        return 0

    def callback_export(self):

        # TODO: Fix!

        if self._debug:
            "DEBUG: export_callback called"

        if len(self._selections) == 0:
            print("No dataset was selected!")
            self.send_status("No dataset was selected!")
            return 1
        elif len(self._selections) > 1:
            print("You cannot select more than one dataset!")
            self.send_status("You cannot select more than one dataset!")
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

        new_df = DataFile(filename=filename, driver=driver, debug=self._debug)
        self._datafiles.append(new_df)
        if new_df.load() == 0:

            # Create the top level item for the file
            top_level_item = QtGui.QTreeWidgetItem(self._treeview)

            top_level_item.setText(0, "")  # Selection
            top_level_item.setText(1, self._datafiles[-1].filename)  # Name

            top_level_item.setFlags(top_level_item.flags() | QtCore.Qt.ItemIsUserCheckable)
            top_level_item.setCheckState(0, QtCore.Qt.Unchecked)

            # TODO: Find the number of datasets somehow -PW
            number_of_datasets = 1

            for i in range(number_of_datasets):

                dataset = new_df.get_dataset(i)

                child_item = QtGui.QTreeWidgetItem(top_level_item)
                child_item.setText(0, "")
                child_item.setText(1, "Dataset #{}".format(i))  # TODO: Dataset naming, maybe use ion name? -PW
                child_item.setText(2, "0")  # Step
                child_item.setText(3, "{}".format(dataset.get_a()))  # Mass
                child_item.setText(4, "{}".format(dataset.get_q()))  # Charge
                child_item.setText(5, "{}".format(dataset.get_i()))  # Current
                child_item.setText(6, "{}".format(dataset.get_npart()))  # Number of particles
                child_item.setText(7, "{}".format(dataset.get_nsteps()))  # Number of steps

                child_item.setFlags(child_item.flags() | QtCore.Qt.ItemIsUserCheckable)
                child_item.setCheckState(0, QtCore.Qt.Unchecked)

                self.open_property_manager(datafile_id=len(self._datafiles) - 1,
                                           dataset_id=i,
                                           debug=self._debug)

            top_level_item.setExpanded(True)

            for i in range(self._treeview.columnCount()):
                self._treeview.resizeColumnToContents(i)

            if self._debug:
                print("DEBUG: load_add_ds_callback: Finished loading.")

        return 0

    def callback_load_new_ds(self):
        """
        Callback for Load Dataset... button
        :return: 
        """

        # TODO: Fix!

        if self._debug:
            print("DEBUG: load_new_ds_callback was called")

        filename, driver = self.get_filename(action='open')

        if filename is None:
            return 1

        new_df = DataFile(filename=filename, driver=driver, debug=self._debug)
        self._datafiles.append(new_df)

        if new_df.load() == 0:

            self._datafiles = [new_df]

            self._treeview.clear()

            # Create the top level item for the file
            top_level_item = QtGui.QTreeWidgetItem(self._treeview)

            top_level_item.setText(0, "")  # Selection
            top_level_item.setText(1, self._datafiles[0].filename)  # Name

            top_level_item.setFlags(top_level_item.flags() | QtCore.Qt.ItemIsUserCheckable)
            top_level_item.setCheckState(0, QtCore.Qt.Unchecked)

            # TODO: Find the number of datasets somehow -PW
            number_of_datasets = 1

            for i in range(number_of_datasets):

                dataset = new_df.get_dataset(i)

                child_item = QtGui.QTreeWidgetItem(top_level_item)
                child_item.setText(0, "")
                child_item.setText(1, "Dataset #{}".format(i))  # TODO: Dataset naming, maybe use ion name? -PW
                child_item.setText(2, "0")  # Step
                child_item.setText(3, "{}".format(dataset.get_a()))  # Mass
                child_item.setText(4, "{}".format(dataset.get_q()))  # Charge
                child_item.setText(5, "{}".format(dataset.get_i()))  # Current
                child_item.setText(6, "{}".format(dataset.get_npart()))  # Number of particles
                child_item.setText(7, "{}".format(dataset.get_nsteps()))  # Number of steps

                child_item.setFlags(child_item.flags() | QtCore.Qt.ItemIsUserCheckable)
                child_item.setCheckState(0, QtCore.Qt.Unchecked)

                self.open_property_manager(datafile_id=len(self._datafiles) - 1,
                                           dataset_id=i,
                                           debug=self._debug)

            top_level_item.setExpanded(True)

            for i in range(self._treeview.columnCount()):
                self._treeview.resizeColumnToContents(i)

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
        self.redraw_plots()

    def callback_properties(self):

        # TODO: Fix!

        if self._debug:
            "DEBUG: properties_callback called"

        if len(self._selections) == 0:
            print("No dataset was selected!")
            self.send_status("No dataset was selected!")
            return 1
        elif len(self._selections) > 1:
            print("You cannot select more than one dataset!")
            self.send_status("You cannot select more than one dataset!")
            return 1

        df_i, ds_i = self.get_selection(self._selections[0])

        self.open_property_manager(datafile_id=df_i, dataset_id=ds_i, debug=True)

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

        # TODO: Update some draw variable -DW

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

        # TODO: Using the removeItem(data_item) method does not work properly, this is a workaround -PW
        self._mainWindowGUI.graphicsView_4.items = []
        self._mainWindowGUI.graphicsView_4.update()

        self.send_status("Views cleared!")

        return 0

    def find_dataset(self, datafile_id, dataset_id):
        return self._datafiles[datafile_id].get_dataset(dataset_id)

    def get_filename(self, action='open'):

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
        if "#" in selection_string:  # "#(item)"
            datafile_index = int(selection_string.lstrip("#"))
            return datafile_index, None
        elif "%" in selection_string:  # "%(parent)/child"
            indices = selection_string.lstrip("%").split("/")
            datafile_index, dataset_index = int(indices[0]), int(indices[1])
            return datafile_index, dataset_index

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

    def open_property_manager(self, datafile_id, dataset_id, debug=False):
        self._pm = PropertyManager(self, datafile_id=datafile_id, dataset_id=dataset_id, debug=debug)
        self._pm.run()

        return 0

    def redraw_plots(self):
        """
        (re)draw the plots that are checked
        :return: 
        """

        if self._debug:
            print("DEBUG: redraw_plots called")

        self.clear_plots()

        if len(self._selections) == 0:
            print("No datasets selected to plot!")
            self.send_status("No datasets selected to plot!")
            return 1

        for selection_string in sorted(self._selections):

            df_i, ds_i = self.get_selection(selection_string)

            # TODO: Do this properly
            if ds_i is None:
                print("Only select datasets!")
                return 1

            dataset = self._datafiles[df_i].get_dataset(ds_i)
            settings = dataset.get_plot_settings(translated=True)
            top_level_item = self._treeview.topLevelItem(df_i)
            this_item = top_level_item.child(ds_i)

            try:
                step = int(settings["step"])
            except ValueError:
                print("redraw_plots: Requested step is not an integer!")
                # This shouldn't happen anymore, but if it does it sets the step to zero -PW
                settings["step"] = 0
                self._datafiles[df_i].get_dataset(ds_i).set_plot_settings(settings)
                this_item.setText(1, str(settings["step"]))

            try:
                dataset.set_step_view(step)
            except Exception as e:
                print("redraw_plots: Exception happened when trying to set step view to: '{}'!".format(step))
                print(e)

            plot_settings = dataset.get_plot_settings(translated=True)

            if self._debug:
                print("DEBUG: Displaying Dataset#{}-{}".format(df_i, ds_i))

            if plot_settings["tl_en"] | plot_settings["tr_en"] | \
               plot_settings["bl_en"] | plot_settings["3d_en"] is False:
                print("No plots for Dataset#{}-{} were enabled".format(df_i, ds_i))
                self.send_status("No plots for Dataset#{}-{} were enabled".format(df_i, ds_i))
                return 1

            # TOP LEFT PLOT:

            if plot_settings["tl_en"]:
                top_left_data = (plot_settings["tl_a"], plot_settings["tl_b"])
                top_left_title = (top_left_data[0] + "-" + top_left_data[1]).upper()

                tl_scatter = pg.ScatterPlotItem(x=dataset.get(top_left_data[0]),
                                                y=dataset.get(top_left_data[1]),
                                                pen=pg.mkPen(self._colors[ds_i]), brush='b', size=1.0, pxMode=True)

                self._mainWindowGUI.graphicsView_1.addItem(tl_scatter)
                self._mainWindowGUI.graphicsView_1.setTitle(top_left_title)
                self._mainWindowGUI.graphicsView_1.repaint()

            # TOP RIGHT PLOT:

            if plot_settings["tr_en"]:
                top_right_data = (plot_settings["tr_a"], plot_settings["tr_b"])
                top_right_title = (top_right_data[0] + "-" + top_right_data[1]).upper()

                tr_scatter = pg.ScatterPlotItem(x=dataset.get(top_right_data[0]),
                                                y=dataset.get(top_right_data[1]),
                                                pen=pg.mkPen(self._colors[ds_i]), brush='b', size=1.0, pxMode=True)

                self._mainWindowGUI.graphicsView_2.addItem(tr_scatter)
                self._mainWindowGUI.graphicsView_2.setTitle(top_right_title)
                self._mainWindowGUI.graphicsView_2.repaint()

            # BOTTOM LEFT PLOT:

            if plot_settings["bl_en"]:
                bottom_left_data = (plot_settings["bl_a"], plot_settings["bl_b"])
                bottom_left_title = (bottom_left_data[0] + "-" + bottom_left_data[1]).upper()

                bl_scatter = pg.ScatterPlotItem(x=dataset.get(bottom_left_data[0]),
                                                y=dataset.get(bottom_left_data[1]),
                                                pen=pg.mkPen(self._colors[ds_i]), brush='b', size=1.0, pxMode=True)

                self._mainWindowGUI.graphicsView_3.addItem(bl_scatter)
                self._mainWindowGUI.graphicsView_3.setTitle(bottom_left_title)
                self._mainWindowGUI.graphicsView_3.repaint()

            # BOTTOM RIGHT (3D) PLOT:

            # Only do a 3D display for data with more than one step and it's enabled
            if dataset.get_nsteps() > 1 and plot_settings["3d_en"]:

                _grid = True  # Always display the grids for now

                for particle_id in range(dataset.get_npart()):
                    particle, _c = dataset.get_particle(particle_id, get_color="random")
                    pts = np.array([particle.get("x"), particle.get("y"), particle.get("z")]).T
                    plt = pg.opengl.GLLinePlotItem(pos=pts, color=pg.glColor(_c), width=1.,
                                                   antialias=True)

                    self._mainWindowGUI.graphicsView_4.addItem(plt)

                if _grid:

                    # TODO: Make the grid size dynamic -PW

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

                    self._mainWindowGUI.graphicsView_4.addItem(gx)
                    self._mainWindowGUI.graphicsView_4.addItem(gy)
                    self._mainWindowGUI.graphicsView_4.addItem(gz)

                self._mainWindowGUI.graphicsView_4.opts["distance"] = 3e-1  # Seems to be a good value for now

        self.send_status("Plotting complete!")

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

    def treeview_clicked(self, item, column):

        if self._debug:
            print("treeview_data_changed callback called with item {} and column {}".format(item, column))

        if column == 0:
            checkstate = (item.checkState(0) == QtCore.Qt.Checked)
            index = self._treeview.indexFromItem(item).row()

            if item.parent() is None:
                selection_string = "#{}".format(index)  # "#" Identifier for a datafile object
            else:
                parent_index = self._treeview.indexFromItem(item.parent()).row()
                selection_string = "%{}/{}".format(parent_index, index)  # "%" Identifier for dataset object

            if checkstate is True and selection_string not in self._selections:
                self._selections.append(selection_string)
            elif checkstate is False and selection_string in self._selections:
                self._selections.remove(selection_string)

        return 0
#
#
# if __name__ == "__main__":
#
#     ppp = PyParticleProcessor(debug=True)
#     ppp.run()
