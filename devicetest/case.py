"""Contain the base class for Tango device unit testing."""

# Imports
import os
import PyTango
import unittest
from devicetest.context import NodbTangoContext

# Device test case
class DeviceTestCase(unittest.TestCase):
    """Base class for TANGO device unit testing."""

    port = 0
    db = "tango.db"
    device_cls = None
    properties = {}

    @classmethod
    def mocking(cls):
        """Mock the librairies. To override."""
        pass
    
    @classmethod
    def setUpClass(cls):
        """Set up device server using the class attributes"""
        # PyTango patch
        PyTango.__leave = lambda *args, **kwargs: None
        # Set up class
        cls.mocking()
        cls._context = NodbTangoContext(cls.device_cls,
                                        properties=cls.properties,
                                        db=cls.db,
                                        port=cls.port
                                        ).start()
        cls.device = cls._context.device
        
    @classmethod
    def tearDownClass(cls):
        """Kill the device server."""
        cls._context.stop(1)
        os.remove(cls.db)

    def setUp(self):
        """Prepare a test environment"""
        self.mocking()
        self.device.Init()

