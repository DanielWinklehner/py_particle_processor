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

        for dataset in self._selections:

            animate = {}

            datasource = dataset.get_datasource()

            nsteps, npart = dataset.get_nsteps(), dataset.get_npart()

            for step in range(nsteps):

                animate["Step#{}".format(step)] = {}

                x_val = np.array(datasource["Step#{}".format(step)]["x"])
                y_val = np.array(datasource["Step#{}".format(step)]["y"])

                # Center the beam
                animate["Step#{}".format(step)]["x"] = x_val - np.mean(x_val)
                animate["Step#{}".format(step)]["y"] = y_val - np.mean(y_val)

        # Handle animations
        last_step = animate["Step#{}".format(nsteps-1)]["x"]
        # x_max = max(np.amin(last_step), np.amax(last_step), key=abs)
        x_max = 0.1
        fig = plt.figure()
        ax = plt.axes(xlim=(-x_max, x_max), ylim=(-x_max, x_max))
        line, = ax.plot([], [], 'ko', ms=.1, alpha=0.6)
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.title("X-Y: {} Steps".format(nsteps-1))

        def init():
            line.set_data([], [])
            return line,

        def update(i):
            x = animate["Step#{}".format(i)]["x"]
            y = animate["Step#{}".format(i)]["y"]

            completed = int(100*(i/(nsteps-1)))
            self._parent.send_status("Animation progress: {}% complete".format(completed))
            line.set_data(x, y)
            return line,

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
