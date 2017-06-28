from ..abstract_tool import AbstractTool
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy


class AnimateXY(AbstractTool):

    def __init__(self, parent):
        super(AnimateXY, self).__init__()
        self._name = "Animate X-Y"
        self._parent = parent

        self._has_gui = False
        self._need_selection = True
        self._min_selections = 1
        self._max_selections = 1
        self._redraw_on_exit = False

    def run(self):
        for dataset in self._selections:
            datasource = dataset.get_datasource()
            # animate = copy.deepcopy(datasource)
            nsteps, npart = dataset.get_nsteps(), dataset.get_npart()

            for step in range(nsteps):

                # Find the average position
                avg_x = sum(datasource["Step#{}".format(step)]["x"])/npart
                avg_y = sum(datasource["Step#{}".format(step)]["y"])/npart
                avg_z = sum(datasource["Step#{}".format(step)]["z"])/npart
                avg_pos = [avg_x, avg_y, avg_z]

                norm = np.linalg.norm(avg_pos)
                diff = np.array([0,norm,0]) - np.array(avg_pos)

                # Center and rotate the beam
                for part in range(npart):
                    for i, key in enumerate(["x", "y", "z"]):
                        datasource["Step#{}".format(step)][key][part] -= avg_pos[i] + diff[i]

        last_step = datasource["Step#{}".format(nsteps)]["x"]
        x_max = max(np.amin(last_step), np.amax(last_step), key=abs)
        fig = plt.figure()
        ax = plt.axes(xlim=(-x_max, x_max), ylim=(-x_max, x_max))
        line, = ax.plot([], [], 'ko')

        def init():
            line.set_data([], [])
            return line,

        def update(i):
            line.set_data(animate["Step#{}".format(i)]["x"], animate["Step#{}".format(i)]["y"])
            return line,

        ani = animation.FuncAnimation(fig, update, init_func=init)
        plt.show()

    def open_gui(self):
        self.run()
