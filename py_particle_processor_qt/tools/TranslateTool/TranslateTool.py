from ..abstract_tool import AbstractTool
from .translatetoolgui import Ui_TranslateToolGUI
from PyQt5 import QtGui


class TranslateTool(AbstractTool):
    def __init__(self, parent):
        super(TranslateTool, self).__init__(parent)
        self._name = "Translate Tool"
        self._parent = parent

        # --- Initialize the GUI --- #
        self._translateToolWindow = QtGui.QMainWindow()
        self._translateToolGUI = Ui_TranslateToolGUI()
        self._translateToolGUI.setupUi(self._translateToolWindow)

        self._translateToolGUI.apply_button.clicked.connect(self.callback_apply)
        self._translateToolGUI.cancel_button.clicked.connect(self.callback_cancel)
        self._translateToolGUI.x_trans.textChanged.connect(self.check_inputs)
        self._translateToolGUI.y_trans.textChanged.connect(self.check_inputs)
        self._translateToolGUI.z_trans.textChanged.connect(self.check_inputs)

        self._has_gui = True
        self._need_selection = True
        self._min_selections = 1
        self._max_selections = None
        self._redraw_on_exit = True
        self._invalid_input = False

    # --- Required Functions --- #

    def run(self):

        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._translateToolWindow.width())
        _y = 0.5 * (screen_size.height() - self._translateToolWindow.height())

        # --- Show the GUI --- #
        self._translateToolWindow.show()
        self._translateToolWindow.move(_x, _y)

    # --- GUI-related Functions --- #

    def open_gui(self):
        self.run()

    def close_gui(self):
        self._translateToolWindow.close()

    def callback_apply(self):
        if self.apply() == 0:
            self._redraw()
            self.close_gui()

    def callback_cancel(self):
        self.close_gui()

    # --- Tool-related Functions --- #

    def check_inputs(self):

        inputs = [self._translateToolGUI.x_trans, self._translateToolGUI.y_trans, self._translateToolGUI.z_trans]
        self._invalid_input = False

        for input_item in inputs:
            translate_txt = input_item.text()

            if len(translate_txt) == 0:
                input_item.setStyleSheet("color: #000000")
                self._invalid_input = True

            try:
                value = float(translate_txt)  # Try to convert the input to a float
                input_item.setStyleSheet("color: #000000")

            except ValueError:

                # Set the text color to red
                input_item.setStyleSheet("color: #FF0000")
                self._invalid_input = True

        return 0

    def apply(self):

        dx, dy, dz = (self._translateToolGUI.x_trans.text(),
                      self._translateToolGUI.y_trans.text(),
                      self._translateToolGUI.z_trans.text())

        self.check_inputs()
        if self._invalid_input:
            return 1

        # Let's do this on a text basis instead of inferring from the indices
        translations = [float(item) for item in [dx, dy, dz]]

        for dataset in self._selections:
            datasource = dataset.get_datasource()
            nsteps, npart = dataset.get_nsteps(), dataset.get_npart()

            for step in range(nsteps):
                for part in range(npart):
                    for i, direction in enumerate(["x", "y", "z"]):
                        datasource["Step#{}".format(step)][direction][part] += translations[i]

        return 0
