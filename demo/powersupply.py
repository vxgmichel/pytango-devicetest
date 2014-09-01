from time import time
from numpy.random import random_sample
import socket


from PyTango import AttrQuality, AttrWriteType, DispLevel
from PyTango.server import Device, DeviceMeta, attribute, command
from PyTango.server import device_property


class PowerSupply(Device):
    """ A power supply device."""
    __metaclass__ = DeviceMeta

    # Properties

    host = device_property(dtype=str, doc="Host name")
    port = device_property(dtype=int, default_value=9788)

    #Attribute

    voltage = attribute()
    current = attribute(label="Current", dtype=float,
                        display_level=DispLevel.EXPERT,
                        access=AttrWriteType.READ_WRITE,
                        unit="A", format="8.4f",
                        min_value=0.0, max_value=8.5,
                        min_alarm=0.1, max_alarm=8.4,
                        min_warning=0.5, max_warning=8.0,
                        doc="The power supply current")
    noise = attribute(label="Noise", dtype=((float,),),
                      max_dim_x=1024, max_dim_y=1024)


    # Device methods

    def init_device(self):
        self.get_device_properties()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(0.5)
        try: self.s.connect((self.host, self.port))
        except: pass

    # Read/write methods

    def read_voltage(self):
        return 10.0

    def read_current(self):
        return 2.3456, time(), AttrQuality.ATTR_WARNING

    def write_current(self, current):
        print("Current set to %f" % current)

    def read_noise(self):
        return random_sample((2,2))

    # Commands

    @command(dtype_in=float)
    def ramp(self, value):
        print("Ramping up...")
