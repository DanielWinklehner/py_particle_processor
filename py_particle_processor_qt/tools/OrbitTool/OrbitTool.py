from ..abstract_tool import AbstractTool
from .orbittoolgui import Ui_OrbitToolGUI
from PyQt5 import QtGui


class OrbitTool(AbstractTool):

    def __init__(self, parent):
        super(OrbitTool, self).__init__(parent)
        self._name = "Orbit Tool"
        self._parent = parent

        # --- Initialize the GUI --- #
        self._orbitToolWindow = QtGui.QMainWindow()
        self._orbitToolGUI = Ui_OrbitToolGUI()
        self._orbitToolGUI.setupUi(self._orbitToolWindow)

        self._orbitToolGUI.apply_button.clicked.connect(self.callback_apply)
        self._orbitToolGUI.cancel_button.clicked.connect(self.callback_cancel)

        self._has_gui = True
        self._need_selection = True
        self._min_selections = 1
        self._max_selections = None
        self._redraw_on_exit = True

        self.values = [None, None, None]

    # --- Required Functions --- #
    
    def run(self):
        
        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._orbitToolWindow.width())
        _y = 0.5 * (screen_size.height() - self._orbitToolWindow.height())

        # --- Show the GUI --- #
        self._orbitToolWindow.show()
        self._orbitToolWindow.move(_x, _y)

    # --- GUI-related Functions --- #

    def open_gui(self):
        self.run()

    def close_gui(self):
        self._orbitToolWindow.close()

    def callback_apply(self):
        if self.apply() == 0:
            self._redraw()
            self.close_gui()

    def callback_cancel(self):
        self.close_gui()

    # --- Tool-related Functions --- #

    def check_step_numbers(self):

        step_texts = [self._orbitToolGUI.step_1, self._orbitToolGUI.step_2,
                      self._orbitToolGUI.step_3]

        self.values = [None, None, None]

        for i, step in enumerate(step_texts):
            s_txt = step.text()
            if len(s_txt) == 0:
                step.setStyleSheet("color: #000000")

            try:
                if "." in s_txt:
                    step.setStyleSheet("color: #FF0000")
                else:
                    self.values[i] = int(s_txt)  # Try to convert the input to an int
                    step.setStyleSheet("color: #000000")

            except ValueError:

                # Set the text color to red
                step.setStyleSheet("color: #FF0000")

    def apply(self):
        
        self.check_step_numbers()

        if None in self.values:
            return 1

        for dataset in self._selections:
            dataset.xy_orbit(self.values)

        return 0
