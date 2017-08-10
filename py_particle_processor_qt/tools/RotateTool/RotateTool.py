from ..abstract_tool import AbstractTool
from .rotatetoolgui import Ui_RotateToolGUI
from PyQt5 import QtGui
import numpy as np

class RotateTool(AbstractTool):
    def __init__(self, parent):
        super(RotateTool, self).__init__(parent)
        self._name = "Rotate Tool"
        self._parent = parent

        # --- Initialize the GUI --- #
        self._rotateToolWindow = QtGui.QMainWindow()
        self._rotateToolGUI = Ui_RotateToolGUI()
        self._rotateToolGUI.setupUi(self._rotateToolWindow)

        self._rotateToolGUI.apply_button.clicked.connect(self.callback_apply)
        self._rotateToolGUI.cancel_button.clicked.connect(self.callback_cancel)

        self._has_gui = True
        self._need_selection = True
        self._min_selections = 1
        self._max_selections = None
        self._redraw_on_exit = True

        self._angle = 0.0

    # --- Required Functions --- #

    def run(self):

        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._rotateToolWindow.width())
        _y = 0.5 * (screen_size.height() - self._rotateToolWindow.height())

        # --- Show the GUI --- #
        self._rotateToolWindow.show()
        self._rotateToolWindow.move(_x, _y)

    # --- GUI-related Functions --- #

    def open_gui(self):
        self.run()

    def close_gui(self):
        self._rotateToolWindow.close()

    def callback_apply(self):
        if self.apply() == 0:
            self._redraw()
            self.close_gui()

    def callback_cancel(self):
        self.close_gui()

    # --- Tool-related Functions --- #

    def check(self):
        value = self._rotateToolGUI.value
        v_txt = value.text()
        if len(v_txt) == 0:
            value.setStyleSheet("color: #000000")
        try:
            self._angle = float(v_txt)
            value.setStyleSheet("color: #000000")

        except ValueError:

            # Set the text color to red
            value.setStyleSheet("color: #FF0000")

    def apply(self):
        self.check()

        # TODO: Radians?
        self._angle = np.deg2rad(self._angle)

        rotation_matrix = np.array([[np.cos(self._angle), -np.sin(self._angle), 0.0],
                                    [np.sin(self._angle), np.cos(self._angle), 0.0],
                                    [0.0, 0.0, 1.0]])

        for dataset in self._selections:

            datasource = dataset.get_datasource()
            nsteps, npart = dataset.get_nsteps(), dataset.get_npart()

            for step in range(nsteps):
                for part in range(npart):

                    position, momentum = np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0])

                    for i, v in enumerate(["x", "y", "z"]):
                        position[i] = datasource["Step#{}".format(step)][v][part]
                    for i, v in enumerate(["px", "py", "pz"]):
                        momentum[i] = datasource["Step#{}".format(step)][v][part]

                    rot_position = np.matmul(rotation_matrix, position)
                    rot_momentum = np.matmul(rotation_matrix, momentum)

                    for i, v in enumerate(["x", "y", "z"]):
                        datasource["Step#{}".format(step)][v][part] = float(rot_position[i])
                    for i, v in enumerate(["px", "py", "pz"]):
                        datasource["Step#{}".format(step)][v][part] = float(rot_momentum[i])

        return 0