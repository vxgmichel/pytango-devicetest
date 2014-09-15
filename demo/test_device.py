"""Contain the tests for the power supply device server."""

# Path
import sys, os
path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.insert(0, os.path.abspath(path))

# Imports
import powersupply
from time import sleep
from mock import MagicMock
from PyTango import DevFailed
from devicetest import DeviceTestCase

# Device test case
class TspDeviceTestCase(DeviceTestCase):
    """Test case for packet generation."""

    device = powersupply.PowerSupply
    properties = {'host':'10.10.10.10'}

    @classmethod
    def mocking(cls):
        """Mock the TSP controller access"""
        cls.random_sample = powersupply.random_sample = MagicMock()
        cls.socket_module = powersupply.socket = MagicMock()
        cls.socket_instance = cls.socket_module.socket.return_value


    def test_properties(self):
        self.assertIn("UNKNOWN", self.device.status())
        connect_function = self.socket_instance.connect
        connect_function.assert_called_with(('10.10.10.10', 9788))

    def test_get_noise(self):
        expected_result = [[1,2],[3,4]]
        self.random_sample.return_value = expected_result
        result = self.device.noise
        self.assertEqual(result.tolist(), expected_result)
        
    def test_side_effects(self):
        with self.assertRaises(DevFailed) as context:
            self.device.current = -1
        expected_message = "value for attribute current is below the minimum"
        self.assertIn(expected_message, str(context.exception))
        with self.assertRaises(DevFailed) as context:
            self.device.current = 10
        expected_message = "value for attribute current is above the maximum"
        self.assertIn(expected_message, str(context.exception))
          

# Main execution  
if __name__ == "__main__":
    import unittest
    unittest.main()
        
