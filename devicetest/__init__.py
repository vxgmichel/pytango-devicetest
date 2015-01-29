"""Resources for Tango device unit testing."""

__all__ = ["DeviceTestCase", "TangoTestContext", "Patcher", "main"]

# Imports
from devicetest.case import DeviceTestCase
from devicetest.context import TangoTestContext
from devicetest.patch import Patcher
from devicetest.case import unittest
main = unittest.main

# Patch
Patcher.patch_device_proxy()
