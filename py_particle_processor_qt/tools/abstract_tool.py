from abc import ABC, abstractmethod

# TODO: WIP


class AbstractTool(ABC):

    def __init__(self, parent):
        self._name = None
        self._parent = parent

        self._has_gui = False
        self._need_selection = False
        self._min_selections = 1
        self._max_selections = 1
        self._selections = None

        self._redraw_on_exit = False
        self._plot_manager = None

    def _redraw(self):
        self._plot_manager.redraw_plot()

    def check_requirements(self):
        if len(self._selections) == 0 and self._need_selection:
            return 1

        if self._min_selections is not None:
            if len(self._selections) < self._min_selections:
                return 1

        if self._max_selections is not None:
            if len(self._selections) > self._max_selections:
                return 1

        return 0

    def name(self):
        return self._name

    def redraw_on_exit(self):
        return self._redraw_on_exit

    @abstractmethod
    def run(self):
        pass

    def set_plot_manager(self, plot_manager):
        self._plot_manager = plot_manager

    def set_selections(self, selections):
        self._selections = selections