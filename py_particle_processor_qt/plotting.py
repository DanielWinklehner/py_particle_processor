from py_particle_processor_qt.gui.plot_settings import Ui_PlotSettingsWindow
from py_particle_processor_qt.gui.default_plot_settings import Ui_DefaultPlotSettingsWindow
from PyQt5 import QtGui

# TODO: Debug prints are old


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
