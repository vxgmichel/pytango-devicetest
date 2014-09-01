"""Contain the context to run a device without a database."""

# Imports
from time import sleep
from ast import literal_eval
from PyTango.server import Device
from importlib import import_module
from argparse import ArgumentParser
from devicetest.context import NodbTangoContext


# Types
def literal_dict(arg):
    return dict(literal_eval(arg))
    
def module(arg):
    return import_module(arg)


# Get device 
def get_device(module):
    """Get the device class from a given module."""
    for value in module.__dict__.itervalues():
        try:
            if value != Device and issubclass(value, Device):
                return value
        except TypeError:
            pass
    raise ValueError('No device class in the given module.')


# Parse command line arguments
def parse_command_line_args():
    """Parse arguments given in command line"""
    desc = "Run a given device on a given port."
    parser = ArgumentParser(description=desc)

    msg = 'module containing the device.'
    parser.add_argument('module', metavar='MODULE',
                        type=module, nargs=1,help=msg)

    msg = "The port to use."
    parser.add_argument('--port', metavar='PORT',
                      type=int, help=msg, default=0)

    msg = "The properties to set as python dict."
    parser.add_argument('--prop', metavar='PROP',
                      type=literal_dict, help=msg, default='{}')


    args = parser.parse_args()
    device = get_device(args.module[0])
    return device, args.port, args.prop

# Main function
def main():
    device, port, properties = parse_command_line_args()
    context = NodbTangoContext(device, 
                               properties=properties, 
                               port=port).start()
    msg = '{0} started on port {1} with properties {2}.'
    print(msg.format(device.__name__, context.port, properties))
    print('Device access: {}'.format(context.get_device_access()))
    print('Server access: {}'.format(context.get_server_access()))
    context.join()
    print("Done.")


# Main execution
if __name__ == "__main__":
    main()
