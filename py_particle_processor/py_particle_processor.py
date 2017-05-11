from dans_pymodules import *
import gi
gi.require_version('Gtk', '3.0')  # nopep8
gi.require_version('Gdk', '3.0')  # nopep8
from gi.repository import Gtk, GLib, GObject, Gdk

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
        self.debug = debug

        # --- Load the GUI from XML file and initialize connections --- #
        self._builder = Gtk.Builder()
        self._builder.add_from_file("py_particle_processor.glade")
        self._builder.connect_signals(self.get_connections())

        # --- Get some widgets from the builder --- #
        self._main_window = self._builder.get_object("main_window")
        self._status_bar = self._builder.get_object("main_statusbar")
        self._log_textbuffer = self._builder.get_object("log_texbuffer")

        self._builder.get_object("plots_alignment").add(MPLCanvasWrapper())

    def about_program_callback(self, menu_item):
        """
        :param menu_item:
        :return:
        """
        if self.debug:
            print("About Dialog called by {}".format(menu_item))

        dialog = self._builder.get_object("about_dialogbox")
        dialog.run()
        dialog.destroy()

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
               }

        return con

    def initialize(self):
        """
        Do all remaining initializations
        :return: 0
        """

        if self.debug:
            print("Called initialize() function.")

        self._status_bar.push(0, "Program Initialized.")

        return 0

    def main_quit(self, widget):
        """
        Shuts down the program (and threads) gracefully.
        :return:
        """

        if self.debug:
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

        if self.debug:
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

        if self.debug:
            print("Called statusbar_changed callback for statusbar {}, ID = {}".format(statusbar, context_id))

        _timestr = time.strftime("%d %b, %Y, %H:%M:%S: ", time.localtime())

        self._log_textbuffer.insert(self._log_textbuffer.get_end_iter(), _timestr + text + "\n")

        return 0

if __name__ == "__main__":

    mydebug = False

    ppp = PyParticleProcessor(debug=mydebug)
    ppp.run()
