from py_particle_processor_qt.propertieswindow import Ui_PropertiesWindow
from PyQt5 import QtGui

# TODO: A better new window handling system would be nice -PW


class PropertyManager(object):

    def __init__(self, parent, datafile_id, dataset_id, debug=False):
        self._datafile_id = datafile_id
        self._dataset_id = dataset_id
        self._settings = parent.find_dataset(self._datafile_id, self._dataset_id).get_plot_settings()
        self._debug = debug
        self._parent = parent

        if self._debug:
            print("DEBUG: Initializing PropertyManager instance")

        self._propWindow = QtGui.QMainWindow()
        self._propWindowGUI = Ui_PropertiesWindow()
        self._propWindowGUI.setupUi(self._propWindow)

        if len(self._settings) > 0:
            self.populate_settings()
        else:
            self.apply_settings()

        self._propWindowGUI.apply_button.clicked.connect(self.apply_callback)
        self._propWindowGUI.cancel_button.clicked.connect(self.cancel_callback)
        self._propWindowGUI.dataset_label.setText("DATASET {}-{}".format(self._datafile_id, self._dataset_id))

    def apply_callback(self):

        if self._debug:
            print("DEBUG: apply_callback called")

        self.apply_settings()
        self._parent.apply_plot_settings(datafile_id=self._datafile_id,
                                         dataset_id=self._dataset_id,
                                         plot_settings=self.get_settings())
        self._propWindow.close()

        return 0

    def apply_settings(self):

        if self._debug:
            print("DEBUG: retrieve_settings called")

        # Step:
        self._settings["step"] = self._propWindowGUI.step_input.value()

        # Top Left:
        self._settings["tl_en"] = self._propWindowGUI.tl_enabled.checkState()
        self._settings["tl_a"] = self._propWindowGUI.tl_combo_a.currentIndex()
        self._settings["tl_b"] = self._propWindowGUI.tl_combo_b.currentIndex()

        # Top Right:
        self._settings["tr_en"] = self._propWindowGUI.tr_enabled.checkState()
        self._settings["tr_a"] = self._propWindowGUI.tr_combo_a.currentIndex()
        self._settings["tr_b"] = self._propWindowGUI.tr_combo_b.currentIndex()

        # Bottom Left:
        self._settings["bl_en"] = self._propWindowGUI.bl_enabled.checkState()
        self._settings["bl_a"] = self._propWindowGUI.bl_combo_a.currentIndex()
        self._settings["bl_b"] = self._propWindowGUI.bl_combo_b.currentIndex()

        # 3D Plot:
        self._settings["3d_en"] = self._propWindowGUI.three_d_enabled.checkState()

    def cancel_callback(self):

        if self._debug:
            print("DEBUG: cancel_callback called")

        self._propWindow.close()

        return 0

    def get_settings(self):
        return self._settings

    def populate_settings(self):

        if self._debug:
            print("DEBUG: populate_settings called")

        # Step:
        self._propWindowGUI.step_input.setValue(self._settings["step"])

        # Top Left:
        self._propWindowGUI.tl_enabled.setCheckState(self._settings["tl_en"])
        self._propWindowGUI.tl_combo_a.setCurrentIndex(self._settings["tl_a"])
        self._propWindowGUI.tl_combo_b.setCurrentIndex(self._settings["tl_b"])

        # Top Right:
        self._propWindowGUI.tr_enabled.setCheckState(self._settings["tr_en"])
        self._propWindowGUI.tr_combo_a.setCurrentIndex(self._settings["tr_a"])
        self._propWindowGUI.tr_combo_b.setCurrentIndex(self._settings["tr_b"])

        # Bottom Left:
        self._propWindowGUI.bl_enabled.setCheckState(self._settings["bl_en"])
        self._propWindowGUI.bl_combo_a.setCurrentIndex(self._settings["bl_a"])
        self._propWindowGUI.bl_combo_b.setCurrentIndex(self._settings["bl_b"])

        # 3D Plot:
        self._propWindowGUI.three_d_enabled.setCheckState(self._settings["3d_en"])

    def run(self):

        if self._debug:
            print("DEBUG: Running PropertyManager")

        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._propWindow.width())
        _y = 0.5 * (screen_size.height() - self._propWindow.height())

        # --- Show the GUI --- #
        self._propWindow.show()
        self._propWindow.move(_x, _y)
