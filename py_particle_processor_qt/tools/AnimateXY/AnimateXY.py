from ..abstract_tool import AbstractTool
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PyQt5.QtWidgets import QFileDialog


# Note: This tool requires ffmpeg installation!!!
class AnimateXY(AbstractTool):

    def __init__(self, parent):
        super(AnimateXY, self).__init__(parent)
        self._name = "Animate X-Y"
        self._parent = parent
        self._filename = ""
        
        self._has_gui = False
        self._need_selection = True
        self._min_selections = 1
        self._max_selections = 1
        self._redraw_on_exit = False

    def run(self):

        self._parent.send_status("Setting up animation...")

        for dataset in self._selections:

            animate = {}

            datasource = dataset.get_datasource()

            nsteps, npart = dataset.get_nsteps(), dataset.get_npart()

            for step in range(nsteps):

                animate["Step#{}".format(step)] = {}

                x_val = np.array(datasource["Step#{}".format(step)]["x"])
                y_val = np.array(datasource["Step#{}".format(step)]["y"])

                px_mean = np.mean(np.array(datasource["Step#{}".format(step)]["px"]))
                py_mean = np.mean(np.array(datasource["Step#{}".format(step)]["py"]))
                theta = np.arccos(py_mean/np.sqrt(np.square(px_mean) + np.square(py_mean)))
                if px_mean < 0:
                    theta = -theta

                # Center the beam
                animate["Step#{}".format(step)]["x"] = x_val - np.mean(x_val)
                animate["Step#{}".format(step)]["y"] = y_val - np.mean(y_val)
                
                # Rotate the beam
                temp_x = animate["Step#{}".format(step)]["x"]
                temp_y = animate["Step#{}".format(step)]["y"]
                animate["Step#{}".format(step)]["x"] = temp_x * np.cos(theta) - temp_y * np.sin(theta)
                animate["Step#{}".format(step)]["y"] = temp_x * np.sin(theta) + temp_y * np.cos(theta)

        # Handle animations
        # last_step = animate["Step#{}".format(nsteps-1)]["x"]
        # x_max = max(np.amin(last_step), np.amax(last_step), key=abs)
        x_max = 40
        fig = plt.figure()
        plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
        plt.rc('text', usetex=True)
        plt.rc('grid', linestyle=':')
        ax = plt.axes(xlim=(-x_max, x_max), ylim=(-x_max, x_max))
        line, = ax.plot([], [], 'ko', ms=.1, alpha=0.6)
        plt.grid()
        ax.set_aspect('equal')
        plt.xlabel("Horizontal (mm)")
        plt.ylabel("Longitudinal (mm)")
        ax.set_title("Beam Cross-Section: Step \#0")

        def init():
            line.set_data([], [])
            return line,

        def update(i):
            x = 1000.0 * animate["Step#{}".format(i)]["x"]
            y = 1000.0 * animate["Step#{}".format(i)]["y"]

            completed = int(100*(i/(nsteps-1)))
            self._parent.send_status("Animation progress: {}% complete".format(completed))
            line.set_data(x, y)
            ax.set_title("Beam Cross-Section: Step \#{}".format(i))
            return line, ax

        ani = animation.FuncAnimation(fig, update, frames=nsteps, init_func=init, repeat=False)

        # Save animation
        writer1 = animation.writers['ffmpeg']
        writer2 = writer1(fps=10, bitrate=1800)
        ani.save(self._filename[0]+".mp4", writer=writer2)
        ani._stop()
        self._parent.send_status("Animation saved successfully!")

    def open_gui(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        self._filename = QFileDialog.getSaveFileName(caption="Saving animation...", options=options,
                                                     filter="Video (*.mp4)")

        self.run()
