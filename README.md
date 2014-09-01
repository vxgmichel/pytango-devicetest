## Synopsis

Resources for Tango device unit testing.
Contain a test context, a test case and a console interface.
It is based on the '-file' tango option in order to run a server without the database.

## Requirement

This package is required:

- PyTango 8.1.2

## Installation

Run: python setup.py install

## Usage

For unit testing, follow these steps:

- Import and inherit from the DeviceTestCase class
- Define the mocking class method to patch external libraries
- Write tests using the device proxy 'self.device' and the mock objects.
- It is possible to change the return values of the mock objects at runtime. 

See the example in the demo for further information. 

For a test context, here is a simple example:

    >>> from devicetest import NodbTangoContext
    >>> with NodbTangoContext(MyDevice, properties={}) as proxy:
    ...     print proxy.voltage

See the code for further information

For a console usage, see the help:

python -m devicetest -h

## Demo

This repository contains a simple demo of the tangodoc extension.
In order to run the tests, run: python test_device.py.
Then take a look at:

- The 'demo/powersupply.py' module. Example of documented HLAPI Device class. 
- The 'demo/test_device.py' module. Contain the unit tests.

## Warning

This package is still in development and has a few limitations:

- Using a test context twice will produce a segmentation fault and stop the execution.
- Properties cannot be changed at runtime. I haven't found any way to access the virtual database.
- Tango events are not supported by the '-file' execution mode.

## Contact

Vincent Michel: vincent.michel@maxlab.lu.se
