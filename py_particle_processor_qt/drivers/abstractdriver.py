from abc import ABC, abstractmethod
import os

# TODO: WIP -PW


class AbstractDriver(ABC):
    def __init__(self):
        self._program_name = None
        self._debug = None

    def get_program_name(self):
        return self._program_name

    @abstractmethod
    def import_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def export_data(self, *args, **kwargs):
        pass

    # Source: http://fa.bianp.net/blog/2013/
    # different-ways-to-get-memory-consumption-or-lessons-learned-from-memory_profiler/
    @staticmethod
    def _memory_usage_ps():
        import subprocess
        out = subprocess.Popen(['ps', 'v', '-p', str(os.getpid())],
                               stdout=subprocess.PIPE).communicate()[0].split("\n")
        vsz_index = out[0].split().index("RSS")
        mem = float(out[1].split()[vsz_index]) / 1024.0
        return mem  # Output in bytes

    # Source: https://stackoverflow.com/questions/2104080/how-to-check-file-size-in-python
    @staticmethod
    def _get_file_size(filename):
        return os.stat(filename).st_size  # Output in bytes

    def check_memory(self, filename):
        current_usage = self._memory_usage_ps()
        file_size = self._get_file_size(filename)
        if current_usage + file_size > 5e8:  # 500 MB
            self.convert_to_h5()
        else:
            return 0

    def convert_to_h5(self):
        pass
