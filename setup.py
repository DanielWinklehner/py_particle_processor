from setuptools import setup, find_packages

setup(name='py_particle_processor',
      version='1.2',
      description='a GUI application to generate or load and export particle data for beam physics',
      url='https://github.com/DanielWinklehner/py_particle_processor',
      author='Daniel Winklehner, Philip Weigel, Maria Yampolskaya',
      author_email='winklehn@mit.edu',
      license='MIT',
      packages=find_packages(),
      package_data={'': ['mainwindow.py', 'propertieswindow.py']},
      include_package_data=True,
      zip_safe=False)
