from dataset import *
from mainwindow import *
from properties import *
from dans_pymodules import MyColors
from PyQt5.QtWidgets import qApp, QFileDialog
from PyQt5 import QtGui, QtCore
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


class PyParticleProcessor(object):
    def __init__(self, debug=False):
        """
        Initialize the GUI
        """
        self._debug = debug
        self._colors = MyColors()
        self._datasets = []
        self._selections = []
        self._last_path = ""
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
        self._mainWindowGUI.actionImport_New.triggered.connect(self.load_new_ds_callback)
        self._mainWindowGUI.actionImport_Add.triggered.connect(self.load_add_ds_callback)
        self._mainWindowGUI.actionUnload_Selected.triggered.connect(self.delete_ds_callback)
        self._mainWindowGUI.actionPlot.triggered.connect(self.plot_callback)
        self._mainWindowGUI.actionProperties.triggered.connect(self.properties_callback)
        self._treeview.itemClicked.connect(self.treeview_clicked)

    def about_program_callback(self, menu_item):
        """
        :param menu_item:
        :return:
        """
        if self._debug:
            print("DEBUG: About Dialog called by {}".format(menu_item))

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

    def delete_ds_callback(self):
        """
        Callback for Delete Dataset... button
        :param widget: 
        :return: 
        """

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
            del self._datasets[j]

        for item in items_to_remove:
            (item.parent() or root).removeChild(item)

        if redraw_flag:
            self.redraw_plots()

        return 0

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

        filename, filetype = QFileDialog.getOpenFileName(self._mainWindow,
                                                         caption="Import dataset...",
                                                         directory=self._last_path,
                                                         filter=filetypes_text,
                                                         options=options)

        if filename == "":
            return None, None

        driver = filetype.split("Files")[0].strip()

        return filename, driver

    def initialize(self):
        """
        Do all remaining initializations
        :return: 0
        """

        if self._debug:
            print("DEBUG: Called initialize() function.")

        self._status_bar.showMessage("Program Initialized.")

        return 0

    def load_add_ds_callback(self, widget):
        """
        Callback for Add Dataset... button
        :param widget: 
        :return: 
        """

        if self._debug:
            print("DEBUG: load_add_ds_callback was called with widget {}".format(widget))

        filename, driver = self.get_filename(action="open")

        if filename is None:
            return 1

        _new_ds = Dataset(debug=self._debug)

        if _new_ds.load_from_file(filename, driver=driver) == 0:

            self._datasets.append(_new_ds)

            # Update the liststore
            new_item = QtGui.QTreeWidgetItem(self._treeview)

            new_item.setText(0, "")
            new_item.setText(1, "0")
            new_item.setText(2, "{}".format(self._datasets[-1].get_a()))
            new_item.setText(3, "{}".format(self._datasets[-1].get_q()))
            new_item.setText(4, "{}".format(self._datasets[-1].get_i()))
            new_item.setText(5, "{}".format(self._datasets[-1].get_npart()))
            new_item.setText(6, "{}".format(self._datasets[-1].get_nsteps()))
            new_item.setText(7, self._datasets[-1].get_filename())

            new_item.setFlags(new_item.flags() | QtCore.Qt.ItemIsUserCheckable)
            new_item.setCheckState(0, QtCore.Qt.Unchecked)

            if self._debug:
                print("DEBUG: load_add_ds_callback: Finished loading.")

        return 0

    def load_new_ds_callback(self):
        """
        Callback for Load Dataset... button
        :param widget: 
        :return: 
        """

        if self._debug:
            print("DEBUG: load_new_ds_callback was called")

        filename, driver = self.get_filename(action='open')

        if filename is None:
            return 1

        _new_ds = Dataset(debug=self._debug)

        if _new_ds.load_from_file(filename, driver=driver) == 0:

            self._datasets = [_new_ds]

            self._treeview.clear()

            new_item = QtGui.QTreeWidgetItem(self._treeview)

            new_item.setText(0, "")
            new_item.setText(1, "0")
            new_item.setText(2, "{}".format(self._datasets[0].get_a()))
            new_item.setText(3, "{}".format(self._datasets[0].get_q()))
            new_item.setText(4, "{}".format(self._datasets[0].get_i()))
            new_item.setText(5, "{}".format(self._datasets[0].get_npart()))
            new_item.setText(6, "{}".format(self._datasets[0].get_nsteps()))
            new_item.setText(7, self._datasets[0].get_filename())

            new_item.setFlags(new_item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable)
            new_item.setCheckState(0, QtCore.Qt.Unchecked)

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

    def notebook_page_changed_callback(self, notebook, page, page_num):
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

    def plot_callback(self):
        self.redraw_plots()

    def properties_callback(self):

        if self._debug:
            "DEBUG: properties_callback called"

        if len(self._selections) == 0:
            print("No dataset was selected!")
            return 1
        elif len(self._selections) > 1:
            print("You cannot select more than one dataset!")

        item = self._datasets[self._selections[0]]

        self._pm = PropertyManager(settings=item.get_plot_settings(), debug=True)
        self._pm.run()

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

        # TODO: Using the removeItem(data_item) method does not work properly, this is a workaround
        self._mainWindowGUI.graphicsView_4.items = []
        self._mainWindowGUI.graphicsView_4.update()

        print("Views cleared")

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
            return 1

        for idx in sorted(self._selections):

            dataset = self._datasets[idx]
            this_item = self._treeview.topLevelItem(idx)

            try:
                step = int(this_item.text(1))
            except ValueError:
                print("redraw_plots: Requested step is not an integer!")
                step = 0
                this_item.setText(1, str(step))

            try:
                dataset.set_step_view(step)
            except Exception as e:
                print("redraw_plots: Exception happened when trying to set step view to: '{}'!".format(step))
                print(e)

            if dataset.get_selected():

                if self._debug:
                    print("DEBUG: Displaying Dataset#{}".format(idx))

                xy_scatter = pg.ScatterPlotItem(x=dataset.get("x"), y=dataset.get("y"),
                                                pen=pg.mkPen(color=self._colors[idx]), brush='b', size=1.0)

                self._mainWindowGUI.graphicsView_1.addItem(xy_scatter)
                self._mainWindowGUI.graphicsView_1.setTitle("XY")
                self._mainWindowGUI.graphicsView_1.repaint()

                xxp_scatter = pg.ScatterPlotItem(x=dataset.get("x"), y=dataset.get("px"),
                                                 pen=pg.mkPen(self._colors[idx]), brush='b', size=1.0, pxMode=True)

                self._mainWindowGUI.graphicsView_2.addItem(xxp_scatter)
                self._mainWindowGUI.graphicsView_2.setTitle("XXP")
                self._mainWindowGUI.graphicsView_2.repaint()

                yyp_scatter = pg.ScatterPlotItem(x=dataset.get("y"), y=dataset.get("py"),
                                                 pen=pg.mkPen(self._colors[idx]), brush='b', size=1.0, pxMode=True)

                self._mainWindowGUI.graphicsView_3.addItem(yyp_scatter)
                self._mainWindowGUI.graphicsView_3.setTitle("YYP")
                self._mainWindowGUI.graphicsView_3.repaint()

                if dataset.get_nsteps() > 1:  # Only do a 3d display for data with more than one step

                    _grid = True  # Always display the grids for now

                    for id in range(dataset.get_npart()):
                        particle, _c = dataset.get_particle(id, get_color="random")
                        pts = np.array([particle.get("x"), particle.get("y"), particle.get("z")]).T
                        plt = pg.opengl.GLLinePlotItem(pos=pts, color=pg.glColor(_c), width=1.,
                                                       antialias=True)

                        self._mainWindowGUI.graphicsView_4.addItem(plt)

                    if _grid:
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

        return 0

    def run(self):
        """
        Run the GUI
        :return: 
        """
        self.initialize()

        # --- Show the GUI --- #
        self._mainWindow.show()

        return 0

    def statusbar_changed_callback(self, statusbar, context_id, text):
        """
        Callback that handles what happens when a message is pushed in the
        statusbar
        """

        if self._debug:
            print("Called statusbar_changed callback for statusbar {}, ID = {}".format(statusbar, context_id))

        _timestr = time.strftime("%d %b, %Y, %H:%M:%S: ", time.localtime())

        self._log_textbuffer.insert(self._log_textbuffer.get_end_iter(), _timestr + text + "\n")

        return 0

    def treeview_clicked(self, item, column):

        if self._debug:
            print("treeview_data_changed callback called with item {} and column {}".format(item, column))

        if column == 0:
            checkstate = (item.checkState(0) == QtCore.Qt.Checked)
            index = self._treeview.indexFromItem(item).row()
            if self._datasets[index].get_selected() != checkstate:
                self._datasets[index].set_selected(checkstate)

            if checkstate is True and index not in self._selections:
                self._selections.append(index)
            elif checkstate is False and index in self._selections:
                self._selections.remove(index)


if __name__ == "__main__":
    application = QtGui.QApplication([])
    ppp = PyParticleProcessor(debug=True)
    ppp.run()
    application.exec_()
