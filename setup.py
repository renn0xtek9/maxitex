#!/usr/bin/python3

#from distutils.core import setup
from setuptools import setup

long_description = """\
maxitex.py 
"""

setup(name='Maxitex',
      version='0.1',
      description='A tool to generate latex out of code embeded in Maxima scripts',
      long_description=long_description,
      author='Maxime Haselbauer',
      author_email='maxime.haselbauer@googlemail.com',
      url='',
      packages=['maxitex'],
      install_requires=[''],
      entry_points = {
	      'console_scripts': [
		      'maximaTex=maxitex.maxitex:main'
		      ],
	      },
     )

