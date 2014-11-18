"""Provide the a singleton to patch PyTango.Proxy."""

# Imports
import PyTango
from mock import Mock

# Singleton decorator
def singleton(cls):
    """Implement the singleton pattern."""
    return cls()

# Patcher singleton
@singleton
class Patcher():
    """Singleton to patch the device proxy class."""

    def __init__(self):
        self.ActualDeviceProxy = None
        msg = "PyTango.DeviceProxy cannot be instanciated "
        msg += "while using the `devicetest` library. "
        msg += "It has to be mocked after importing `devicetest`."
        error = NotImplementedError(msg)
        self.MockDeviceProxy = Mock(name="DeviceProxy",
                                    side_effect=error)
    
    def patch_device_proxy(self):
        """Mock the device prxy class and return it."""
        if self.ActualDeviceProxy is None:
            self.ActualDeviceProxy = PyTango.DeviceProxy
            PyTango.DeviceProxy = self.MockDeviceProxy
        return PyTango.DeviceProxy
        
    def unpatch_device_proxy():
        """Unmock the device prxy class and return it."""
        if ActualDeviceProxy is not None:
            PyTango.DeviceProxy = self.ActualDeviceProxy
            self.ActualDeviceProxy = None
        return PyTango.DeviceProxy

    def __enter__(self):
        """Enter method for context support."""
        return self.patch_device_proxy()

    def __exit__(self, exc_type, exception, trace):
        """Exit method for context support."""
        unpatch_device_proxy()
