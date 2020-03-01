#!/usr/bin/env python3
from setuptools import setup

setup(name='bliptools',
      install_requires = ['numpy',
                          'matplotlib',
                          'cartopy',
                          'requests',
                          'sqlalchemy',],
      version='0.0.1',
      description='tools for handling blipfoto journals',
      author='Magnus Hagdorn',
      author_email='magnus.hagdorn@marsupium.org',
      url='https://github.com/mhagdorn/bliptools',
      packages=['bliptools'],
      entry_points={
          'console_scripts': [
              'bliptools-update = bliptools.update:main',
              'bliptools-map = bliptools.map:main'
              ],
      },
  )
