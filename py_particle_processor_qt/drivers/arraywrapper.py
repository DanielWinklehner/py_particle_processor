import numpy as np


class ArrayWrapper(object):

    def __init__(self, array_like):
        if type(array_like) is not np.array:
            self._array = np.array(array_like)
        else:
            self._array = array_like

    def __get__(self):
        return self

    def __getitem__(self, key):
        return self._array[key]

    def __setitem__(self, key, item):
        self._array[key] = item

    def __len__(self):
        return len(self._array)

    @property
    def value(self):
        return self._array

    def append(self, value):
        self._array = np.append(self._array, value)