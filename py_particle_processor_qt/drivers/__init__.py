from py_particle_processor_qt.drivers.OPALDriver import *
from py_particle_processor_qt.drivers.TraceWinDriver import *
from py_particle_processor_qt.drivers.COMSOLDriver import *
from py_particle_processor_qt.drivers.IBSimuDriver import *

"""
The driver mapping contains the information needed for the ImportExportDriver class to wrap around the drivers
Rules: 
key has to be unique and one continuous 'word'
several extensions can be specified for one driver 
"""
driver_mapping = {'OPAL': {'driver': OPALDriver,
                           'extensions': ['.h5', '.dat']},
                  'TraceWin': {'driver': TraceWinDriver,
                               'extensions': ['.txt', '.dat']},
                  'COMSOL': {'driver': COMSOLDriver,
                             'extensions': ['.txt']},
                  'IBSimu': {'driver': IBSimuDriver,
                             'extensions': ['.txt']}
                  }
