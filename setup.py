#!/usr/bin/env python3
from setuptools import setup

setup(name='bliptools',
      install_requires = ['numpy',
                          'matplotlib',
                          'cartopy',
                          'geojson',
                          'requests',
                          'folium',
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
              'bliptools-map = bliptools.map:main',
              'bliptools-geojson = bliptools.togeojson:main',
              'bliptools-info = bliptools.info:main',
              'bliptools-folium = bliptools.folium:main',
          ],
      },
  )
