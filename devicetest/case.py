"""Contain the base class for Tango device unit testing."""

# Imports
import os
import PyTango
import unittest
from devicetest.context import TangoTestContext

# Device test case
class DeviceTestCase(unittest.TestCase):
    """Base class for TANGO device unit testing."""

    port = 0
    db = "tango.db"
    device_cls = None
    properties = {}
    teardown_timeout = 1.0

    @classmethod
    def mocking(cls):
        """Mock the librairies. To override."""
        pass
    
    @classmethod
    def setUpClass(cls):
        """Set up device server using the class attributes"""
        cls.mocking()
        cls._context = TangoTestContext(cls.device_cls,
                                        properties=cls.properties,
                                        db=cls.db,
                                        port=cls.port
                                        ).start()
        cls.device = cls._context.device
        
    @classmethod
    def tearDownClass(cls):
        """Kill the device server."""
        cls._context.stop(cls.teardown_timeout)
        os.remove(cls.db)

    def setUp(self):
        """Prepare a test environment"""
        self.mocking()
        self.device.Init()

