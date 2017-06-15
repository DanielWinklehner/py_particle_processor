from abc import ABC, abstractmethod

# TODO: WIP

class AbstractTool(ABC):

    def __init__(self, selections):
        self._name = None
        self._need_selection = False
        self._num_selections = 1
        self._selections = selections

    @abstractmethod
    def run(self):
        pass

    def name(self):
        return self._name

    def needs_selection(self):
        return self._need_selection

    def num_selections(self):
        return self._num_selections
