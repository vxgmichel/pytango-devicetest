## Synopsis

Resources for Tango device unit testing.
It is based on the '--file' tango option to run a server without database.

## Content

- A tango test context
- A unittest case
- A console interface.

## Requirement

- PyTango >= 8.1.1

## Compatibility

The device test case is fully compatible with nosetests and its collector
'nosetests.collector' for the 'test_suite' setuptools option.

## Installation

Run: python setup.py install

## Test context usage

Consider this simple example:

    >>> from devicetest import TangoTestContext
    >>> from MyServer import MyDevice
    >>> prop = {"host":"10.10.10.10"}
    >>> with TangoTestContext(MyDevice, properties=prop) as proxy:
    ...     print proxy.voltage

See the code for further information

## Unit testing usage

Follow these steps:

- Import and inherit from the DeviceTestCase class
- Define the mocking class method to patch external libraries
- Write tests using the device proxy 'self.device' and the mock objects.
- It is possible to change the return values of the mock objects at runtime. 

Note that the server is started only once. The Init command and the mocking 
class method are called before each tests. That way, every test should be 
independant from one another.

See the example in the demo for further information. 

## Console usage

The console interface is useful to run a device with given properties but
without the TANGO database. It displays the device and server proxy access
names in order to access the device from somewhere else.

Consider this example:

    usr@machine:/~python-devicetest$ python -m devicetest demo.powersupply 
    --prop "{'host':'10.10.10.10'}" --port 10001
    Ready to accept request
    PowerSupply started on port 10001 with properties {'host': '10.10.10.10'}.
    Device access: localhost:10001/test/nodb/powersupply#dbase=no
    Server access: localhost:10001/dserver/PowerSupply/powersupply#dbase=no

Or see the help:

    usr@machine:/~python-devicetest$ python -m devicetest -h

Note that this package also include a port detection feature.
If 0 or no port is given, the context object will pick a random free port 
between 1024 to 65535. However, note that the port is not guaranteed to stay
available between the moment it is picked and the moment it is used.

## Demo

This repository contains a simple demo of the device test case.
In order to run the tests, run: 

    usr@machine:/~python-devicetest$ python demo/test_device.py.

Then take a look at:

- The 'demo/powersupply.py' module. Example of documented HLAPI Device class. 
- The 'demo/test_device.py' module. Contain the unit tests.

Note that these 3 tests should run in less than 50 ms. 
Even for a more complicated Tango device, if all the external libraries are 
patched, the execution shoudn't take more than a few hundred milliseconds.
This makes it valid unitesting for continuous integration.

## Warning

This package is still in development and has a few limitations:

- Using a test context twice will produce a segmentation fault 
  and stop the execution.
- Properties cannot be changed at runtime. 
  I haven't found a single way to access the virtual database.
- Tango events are not supported by the '--file' execution mode.
  See the Tango documentation for further information.
- Sadly, it is not compatible with the coverage tool "coverage". 
  This is because the Tango layers mess up with the coverage collector.

## Contact

Vincent Michel: vincent.michel@maxlab.lu.se
