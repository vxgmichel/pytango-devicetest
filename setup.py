#!/usr/bin/env python

from setuptools import setup

setup(name="python-devicetest",
      version="0.1.4",
      description="Resources for Tango device unit testing.",
      packages=['devicetest'],
      install_requires=['unittest2'],
      )
