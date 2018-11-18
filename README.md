# PyParticleProcessor
Cave: This module is in a rough pre-alpha stage! Comments and Collaborators very welcome, though!

## Introduction
The PyParticleProcessor is a QT5/python3 based tool with a GUI to import and export ion beam information (particle data) from various different simulation packages. There is some limited functionality for plotting these particle data and calculate emittances and Twiss parameters. Users can add their own "drivers" both for analysis tools and import/export.

## Currently Supported Programs
Cave: These are all limited support and need to be expanded. Many of those software packages give the user freedom on how to export data themselves, so care has to be taken to export in the same manor. 
  * [OPAL](https://gitlab.psi.ch/OPAL/src/wikis/home)
  * [TraceWin](http://irfu.cea.fr/dacm/en/logiciels/index.php)
  * [Track](https://www.phy.anl.gov/atlas/TRACK)
  * [COMSOL](https://www.comsol.com/)
  * [IBSimu](http://ibsimu.sourceforge.net/)
  
## Installation
### Windows
Prerequisites are:
  * [Qt5 (Open Source)](https://www.qt.io/download)
  * [dans_pymodules](https://github.com/DanielWinklehner/dans_pymodules)
  
PyPI packages:
  * numpy
  * scipy
  * pyqtgraph
  * PyQt5 (pyqt in Anaconda3)
  * h5py
  * matplotlib
  * pyopengl

The easiest method is to install [Anaconda3](https://www.anaconda.com/download/), create a new virtual environment, then download all the packages listed under PyPI packages inside the virtual environment. Install Qt5 for Windows from the link above and install dans_pymodules from github using pip: From the Anaconda navigator open a terminal running the virtual environment you created earlier ("Open Terminal" from the green triangle next to the new virtual environment's name). Then run pip install like so:

`pip install git+https://github.com/DanielWinklehner/dans_pymodules.git` 

Clone the py_particle_processor repositroy:

`git clone https://github.com/DanielWinklehner/py_particle_processor.git`

For a test you can now run the PyParticleProcessor as a module from the top level directory of this repository:

`python -m py_particle_processor_qt.test`

or you can install the module (also from the top level directory in the repository):

`pip install .`

and write a small test program

### Linux
TODO

### MacOS 
I have no idea :D feel free to let me know how to do it...
