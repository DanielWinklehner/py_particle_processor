from ..abstract_tool import AbstractTool
from .scaletoolgui import Ui_ScaleToolGUI
from PyQt5 import QtGui


class ScaleTool(AbstractTool):

    def __init__(self, parent):
        super(ScaleTool, self).__init__(parent)
        self._name = "Scale Tool"
        self._parent = parent

        # --- Initialize the GUI --- #
        self._scaleToolWindow = QtGui.QMainWindow()
        self._scaleToolGUI = Ui_ScaleToolGUI()
        self._scaleToolGUI.setupUi(self._scaleToolWindow)

        self._scaleToolGUI.apply_button.clicked.connect(self.callback_apply)
        self._scaleToolGUI.cancel_button.clicked.connect(self.callback_cancel)
        self._scaleToolGUI.scaling_factor.textChanged.connect(self.check_scaling_factor)

        self._has_gui = True
        self._need_selection = True
        self._min_selections = 1
        self._max_selections = None
        self._redraw_on_exit = True

    # --- Required Functions --- #
    
    def run(self):
        
        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._scaleToolWindow.width())
        _y = 0.5 * (screen_size.height() - self._scaleToolWindow.height())

        # --- Show the GUI --- #
        self._scaleToolWindow.show()
        self._scaleToolWindow.move(_x, _y)

    # --- GUI-related Functions --- #

    def open_gui(self):
        self.run()

    def close_gui(self):
        self._scaleToolWindow.close()

    def callback_apply(self):
        if self.apply() == 0:
            self._redraw()
            self.close_gui()

    def callback_cancel(self):
        self.close_gui()

    # --- Tool-related Functions --- #

    def check_scaling_factor(self):

        scale_txt = self._scaleToolGUI.scaling_factor.text()

        if len(scale_txt) == 0:
            self._scaleToolGUI.scaling_factor.setStyleSheet("color: #000000")
            return None

        try:
            value = float(scale_txt)  # Try to convert the input to a float
            self._scaleToolGUI.scaling_factor.setStyleSheet("color: #000000")
            return value

        except ValueError:

            # Set the text color to red
            self._scaleToolGUI.scaling_factor.setStyleSheet("color: #FF0000")
            return None

    def apply(self):
        
        prop_txt = self._scaleToolGUI.parameter_combo.currentText()
        scaling_factor = self.check_scaling_factor()

        if scaling_factor is None:
            return 1
        
        # Let's do this on a text basis instead of inferring from the indices
        properties = [t.rstrip(",").lower() for t in prop_txt.split(" ") if "(" not in t]

        for dataset in self._selections:
            datasource = dataset.get_datasource()
            nsteps, npart = dataset.get_nsteps(), dataset.get_npart()

            for step in range(nsteps):
                for part in range(npart):
                    for prop in properties:
                        datasource["Step#{}".format(step)][prop][part] *= scaling_factor

        return 0
