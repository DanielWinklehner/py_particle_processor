import gi
gi.require_version('Gtk', '3.0')  # nopep8
gi.require_version('Gdk', '3.0')  # nopep8
# from gi.repository import Gtk, GLib, GObject, Gdk
from dataset import *

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

        # --- Load the GUI from XML file and initialize connections --- #
        self._builder = Gtk.Builder()
        self._builder.add_from_file("py_particle_processor.glade")
        self._builder.connect_signals(self.get_connections())

        # --- Get some widgets from the builder --- #
        self._main_window = self._builder.get_object("main_window")
        self._status_bar = self._builder.get_object("main_statusbar")
        self._log_textbuffer = self._builder.get_object("log_texbuffer")
        self._datasets_ls = self._builder.get_object("species_ls")
        self._datasets_tv = self._builder.get_object("species_tv")

        self._main_plot_axes = MPLCanvasWrapper(main_window=self._main_window)
        self._builder.get_object("plots_alignment").add(self._main_plot_axes)

        # --- Create some CellRenderers for the Species TreeView
        _i = 0
        for item in ["mass_tvc", "charge_tvc", "current_tvc", "np_tvc", "filename_tvc"]:
            _i += 1
            crt = Gtk.CellRendererText()
            self._builder.get_object(item).pack_start(crt, False)
            self._builder.get_object(item).add_attribute(crt, "text", _i)

        crtog = Gtk.CellRendererToggle()
        self._builder.get_object("toggle_tvc").pack_start(crtog, True)
        self._builder.get_object("toggle_tvc").add_attribute(crtog, "active", 0)

        crtog.connect("toggled", self.cell_toggled, self._datasets_ls, "dat")

        self._datasets = []

    def about_program_callback(self, menu_item):
        """
        :param menu_item:
        :return:
        """
        if self._debug:
            print("About Dialog called by {}".format(menu_item))

        dialog = self._builder.get_object("about_dialogbox")
        dialog.run()
        dialog.destroy()

        return 0

    def cell_toggled(self, widget, path, model, mode):
        """
        Callback function for toggling one of the checkboxes in the species
        TreeView. Updates the View and refreshes the plots...
        """
        if self._debug:
            print("cell_toggled was called with widget {} and mode {}".format(widget, mode))

        model[path][0] = not model[path][0]

        # TODO: Update some draw variable -DW

        return 0

    def delete_ds_callback(self, widget):
        """
        Callback for Delete Dataset... button
        :param widget: 
        :return: 
        """

        if self._debug:
            print("delete_ds_callback was called with widget {}".format(widget))

        path, focus = self._datasets_tv.get_cursor()
        del_iter = self._datasets_ls.get_iter(path)

        self._datasets[path[0]].close()
        self._datasets.pop(path[0])

        self._datasets_ls.remove(del_iter)

        return 0

    def get_connections(self):
        """
        This just returns a dictionary of connections
        :return:
        """
        con = {"main_quit": self.main_quit,
               "notebook_page_changed": self.notebook_page_changed_callback,
               "on_main_statusbar_text_pushed": self.statusbar_changed_callback,
               "about_program_menu_item_activated": self.about_program_callback,
               "on_load_dataset_activate": self.load_new_ds_callback,
               "on_add_dataset_activate": self.load_add_ds_callback,
               "on_delete_dataset_activate": self.delete_ds_callback,
               }

        return con

    def initialize(self):
        """
        Do all remaining initializations
        :return: 0
        """

        if self._debug:
            print("Called initialize() function.")

        self._status_bar.push(0, "Program Initialized.")

        return 0

    def load_add_ds_callback(self, widget):
        """
        Callback for Add Dataset... button
        :param widget: 
        :return: 
        """

        if self._debug:
            print("load_add_ds_callback was called with widget {}".format(widget))

        _fd = FileDialog()
        filename = _fd.get_filename(action="open", parent=self._main_window)

        print(filename)

        if filename is None:
            return 0

        _new_ds = Dataset(debug=self._debug)
        _new_ds.load_from_file(filename)

        self._datasets.append(_new_ds)

        # Update the liststore
        self._datasets_ls.append([False,
                                  self._datasets[0].get_a(),
                                  self._datasets[0].get_q(),
                                  self._datasets[0].get_i(),
                                  self._datasets[0].get_npart(),
                                  self._datasets[0].get_filename()]
                                 )

        if self._debug:
            print("load_new_ds_callback: Finished loading.")

        return 0

    def load_new_ds_callback(self, widget):
        """
        Callback for Load Dataset... button
        :param widget: 
        :return: 
        """

        if self._debug:
            print("load_new_ds_callback was called with widget {}".format(widget))

        _fd = FileDialog()
        filename = _fd.get_filename(action="open", parent=self._main_window)

        print(filename)

        if filename is None:
            return 0

        _new_ds = Dataset(debug=self._debug)
        _new_ds.load_from_file(filename)

        self._datasets = [_new_ds]

        # Update the liststore (should be called dataset_ls...)
        self._datasets_ls.clear()
        self._datasets_ls.append([False,
                                  self._datasets[0].get_a(),
                                  self._datasets[0].get_q(),
                                  self._datasets[0].get_i(),
                                  self._datasets[0].get_npart(),
                                  self._datasets[0].get_filename()]
                                 )

        if self._debug:
            print("load_new_ds_callback: Finished loading.")

        return 0

    def main_quit(self, widget):
        """
        Shuts down the program (and threads) gracefully.
        :return:
        """

        if self._debug:
            print("Called main_quit for {}".format(widget))

        self._main_window.destroy()

        Gtk.main_quit()

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
            print("Debug: Notebook {} changed page to {} (page_num = {})".format(notebook,
                                                                                 page,
                                                                                 page_num))
        return 0

    def run(self):
        """
        Run the GUI
        :return: 
        """
        self.initialize()

        # --- Show the GUI --- #
        self._main_window.maximize()
        self._main_window.show_all()

        Gtk.main()

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

if __name__ == "__main__":

    mydebug = True

    ppp = PyParticleProcessor(debug=mydebug)
    ppp.run()
