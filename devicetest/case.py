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
    device = None
    device_cls = None
    properties = {}

    db = ".tangodb"
    debug = 0
    teardown_timeout = 1.0
    daemon_thread = False

    @classmethod
    def mocking(cls):
        """Mock the librairies. To override."""
        pass
    
    @classmethod
    def setUpClass(cls):
        """Set up device server using the class attributes"""
        # Mandatory class attributes
        if cls.device is None:
            raise ValueError("No Tango device given.")
        # Mocking and context
        cls.mocking()
        cls._context = TangoTestContext(cls.device,
                                        cls.device_cls,
                                        properties=cls.properties,
                                        db=cls.db,
                                        port=cls.port,
                                        debug=cls.debug,
                                        daemon=cls.daemon_thread,
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


# Windows patch
import platform
if platform.system() == "Windows":
    DeviceTestCase.teardown_timeout = 0.0
    DeviceTestCase.daemon_thread = True

