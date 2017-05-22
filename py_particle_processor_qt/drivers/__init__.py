from .OPALDriver import *
from .TraceWinDriver import *
from .COMSOLDriver import *

"""
The driver mapping contains the information needed for the ImportExportDriver class to wrap around the drivers
Rules: 
key has to be unique and one continuous 'word'
several extensions can be specified for one driver 
"""
driver_mapping = {'OPAL': {'driver': OPALDriver,
                           'extensions': ['.h5']},
                  'TraceWin': {'driver': TraceWinDriver,
                               'extensions': ['.txt', '.dat']},
                  'COMSOL': {'driver': COMSOLDriver,
                             'extensions': ['.txt']}
                  }
