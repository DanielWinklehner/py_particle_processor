from ..abstract_tool import AbstractTool
from .animateXYgui import Ui_Animate
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import LinearLocator
from PyQt5.QtWidgets import QFileDialog, QMainWindow


# Note: This tool requires ffmpeg installation!!!
class AnimateXY(AbstractTool):

    def __init__(self, parent):
        super(AnimateXY, self).__init__(parent)
        self._name = "Animate X-Y"
        self._parent = parent
        self._filename = ""
        self._settings = {}

        # --- Initialize the GUI --- #
        self._animateWindow = QMainWindow()
        self._animateGUI = Ui_Animate()
        self._animateGUI.setupUi(self._animateWindow)

        self._animateGUI.buttonBox.accepted.connect(self.callback_apply)
        self._animateGUI.buttonBox.rejected.connect(self._animateWindow.close)

        self._has_gui = True
        self._need_selection = True
        self._min_selections = 1
        self._max_selections = 1
        self._redraw_on_exit = False

    def apply_settings(self):
        self._settings["local"] = self._animateGUI.radioButton.isChecked()
        self._settings["global"] = self._animateGUI.radioButton_2.isChecked()
        self._settings["lim"] = float(self._animateGUI.lim.text())
        self._settings["fps"] = int(self._animateGUI.fps.text())

    @staticmethod
    def get_bunch_in_local_frame(datasource, step):
        x = np.array(datasource["Step#{}".format(step)]["x"])
        y = np.array(datasource["Step#{}".format(step)]["y"])
        x_mean = np.mean(x)
        y_mean = np.mean(y)

        px_mean = np.mean(np.array(datasource["Step#{}".format(step)]["px"]))
        py_mean = np.mean(np.array(datasource["Step#{}".format(step)]["py"]))

        theta = np.arccos(py_mean / np.sqrt(np.square(px_mean) + np.square(py_mean)))

        if px_mean < 0:
            theta = -theta

        # Center the beam
        x -= x_mean
        y -= y_mean

        # Rotate the beam and return
        temp_x = x
        temp_y = y

        return temp_x * np.cos(theta) - temp_y * np.sin(theta),  temp_x * np.sin(theta) + temp_y * np.cos(theta)

    def callback_apply(self):
        self.apply_settings()
        self._animateWindow.close()
        self.run_animation()

    def run_animation(self):

        self._parent.send_status("Setting up animation...")

        dataset = self._selections[0]

        animate = {}

        datasource = dataset.get_datasource()

        nsteps, npart = dataset.get_nsteps(), dataset.get_npart()

        # TODO: Total hack, but I want to tag certain particles RIGHT NOW -DW
        tag_step = 568
        tag_y_lim = 5.0 * 1.0e-3  # m
        _x, _y = self.get_bunch_in_local_frame(datasource, tag_step)
        tag_idx = np.where(_y >= tag_y_lim)
        pids = np.array(datasource["Step#{}".format(tag_step)]["id"][tag_idx])

        for step in range(nsteps):

            animate["Step#{}".format(step)] = {"x": np.array(datasource["Step#{}".format(step)]["x"]),
                                               "y": np.array(datasource["Step#{}".format(step)]["y"]),
                                               "id": np.array(datasource["Step#{}".format(step)]["id"])}

            if self._settings["local"]:

                animate["Step#{}".format(step)]["x"], animate["Step#{}".format(step)]["y"] = \
                    self.get_bunch_in_local_frame(datasource, step)

                # px_mean = np.mean(np.array(datasource["Step#{}".format(step)]["px"]))
                # py_mean = np.mean(np.array(datasource["Step#{}".format(step)]["py"]))
                # theta = np.arccos(py_mean/np.sqrt(np.square(px_mean) + np.square(py_mean)))
                # if px_mean < 0:
                #     theta = -theta
                #
                # # Center the beam
                # animate["Step#{}".format(step)]["x"] = x_val - np.mean(x_val)
                # animate["Step#{}".format(step)]["y"] = y_val - np.mean(y_val)
                #
                # # Rotate the beam
                # temp_x = animate["Step#{}".format(step)]["x"]
                # temp_y = animate["Step#{}".format(step)]["y"]
                # animate["Step#{}".format(step)]["x"] = temp_x * np.cos(theta) - temp_y * np.sin(theta)
                # animate["Step#{}".format(step)]["y"] = temp_x * np.sin(theta) + temp_y * np.cos(theta)

        # Handle animations
        fig = plt.figure()
        plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
        plt.rc('text', usetex=True)
        plt.rc('grid', linestyle=':')
        ax = plt.axes(xlim=(-self._settings["lim"], self._settings["lim"]),
                      ylim=(-self._settings["lim"], self._settings["lim"]))
        line1, = ax.plot([], [], 'ko', ms=.1, alpha=0.6)
        line2, = ax.plot([], [], 'ko', ms=.1, alpha=0.8, color='red')
        plt.grid()
        ax.set_aspect('equal')
        if self._settings["local"]:
            plt.xlabel("Horizontal (mm)")
            plt.ylabel("Longitudinal (mm)")
        else:
            plt.xlabel("X (mm)")
            plt.ylabel("Y (mm)")
        ax.set_title(r"Beam Cross-Section: Step \#0")
        ax.get_xaxis().set_major_locator(LinearLocator(numticks=13))
        ax.get_yaxis().set_major_locator(LinearLocator(numticks=13))

        def init():
            line1.set_data([], [])
            line2.set_data([], [])
            return line1, line2,

        def update(i):

            tags = np.isin(animate["Step#{}".format(i)]["id"], pids)

            # Regular Data
            x = 1000.0 * animate["Step#{}".format(i)]["x"][np.invert(tags.astype(bool))]
            y = 1000.0 * animate["Step#{}".format(i)]["y"][np.invert(tags.astype(bool))]

            # Tagged Data
            xt = 1000.0 * animate["Step#{}".format(i)]["x"][tags.astype(bool)]
            yt = 1000.0 * animate["Step#{}".format(i)]["y"][tags.astype(bool)]

            completed = int(100*(i/(nsteps-1)))
            self._parent.send_status("Animation progress: {}% complete".format(completed))
            line1.set_data(x, y)
            line2.set_data(xt, yt)
            ax.set_title(r"Beam Cross-Section: Step \#{}".format(i))
            return line1, line2, ax

        ani = animation.FuncAnimation(fig, update, frames=nsteps, init_func=init, repeat=False)

        # Save animation
        writer1 = animation.writers['ffmpeg']
        writer2 = writer1(fps=self._settings["fps"], bitrate=1800)
        ani.save(self._filename[0]+".mp4", writer=writer2)
        ani._stop()
        self._parent.send_status("Animation saved successfully!")

    def run(self):
        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._animateWindow.width())
        _y = 0.5 * (screen_size.height() - self._animateWindow.height())

        # --- Show the GUI --- #
        self._animateWindow.show()
        self._animateWindow.move(_x, _y)

    def open_gui(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        self._filename = QFileDialog.getSaveFileName(caption="Saving animation...", options=options,
                                                     filter="Video (*.mp4)")

        self.run()
