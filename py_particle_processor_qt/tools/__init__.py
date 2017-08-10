from py_particle_processor_qt.tools.ScaleTool import *
from py_particle_processor_qt.tools.TranslateTool import *
from py_particle_processor_qt.tools.AnimateXY import *
from py_particle_processor_qt.tools.BeamChar import *
from py_particle_processor_qt.tools.CollimOPAL import *
from py_particle_processor_qt.tools.OrbitTool import *
# from py_particle_processor_qt.tools.SpiralGeometry import *
from py_particle_processor_qt.tools.RotateTool import *
"""
Format: {"Object_Name": ("Display Name", object)}
"""
tool_mapping = {"Scale_Tool": ("Scale", ScaleTool),
                "Translate_Tool": ("Translate", TranslateTool),
                "Animate_XY": ("Animate X-Y", AnimateXY),
                "Beam_Characteristics": ("Beam Characteristics", BeamChar),
                "Collim_OPAL": ("Generate Collimator", CollimOPAL),
                "Orbit_Tool": ("Orbit Tool", OrbitTool),
                # "Spiral_Geometry": ("Spiral Geometry", SpiralGeometry),
                "Rotate_Tool": ("Rotate", RotateTool)}
