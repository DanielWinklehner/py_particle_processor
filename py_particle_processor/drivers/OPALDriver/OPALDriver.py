

class OPALDriver:

    def __init__(self, debug=False):
        self._debug = debug
        self._program_name = "OPAL"

    def get_program_name(self):
        return self._program_name

    def import_data(self, data):

        if self._debug:
            print("Importing data from program: {}".format(self._program_name))

        return data

    def export_data(self, data):

        if self._debug:
            print("Exporting data for program: {}".format(self._program_name))

        return data
