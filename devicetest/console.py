"""Contain the context to run a device without a database."""

# Imports
from ast import literal_eval
from importlib import import_module
from argparse import ArgumentParser
from devicetest.context import TangoTestContext


# Types

def literal_dict(arg):
    return dict(literal_eval(arg))


def device(path):
    """Get the device class from a given module."""
    module_name, device_name = path.rsplit(".", 1)
    module = import_module(module_name)
    return getattr(module, device_name)


# Parse command line arguments
def parse_command_line_args():
    """Parse arguments given in command line"""
    desc = "Run a given device on a given port."
    parser = ArgumentParser(description=desc)

    msg = 'The device to run as a python path.'
    parser.add_argument('device', metavar='DEVICE',
                        type=device, help=msg)

    msg = "The port to use."
    parser.add_argument('--port', metavar='PORT',
                        type=int, help=msg, default=0)

    msg = "The debug level."
    parser.add_argument('--debug', metavar='DEBUG',
                        type=int, help=msg, default=0)

    msg = "The properties to set as python dict."
    parser.add_argument('--prop', metavar='PROP',
                        type=literal_dict, help=msg, default='{}')

    args = parser.parse_args()
    return args.device, args.port, args.prop, args.debug


# Main function
def main():
    device, port, properties, debug = parse_command_line_args()
    context = TangoTestContext(device,
                               properties=properties,
                               port=port,
                               debug=debug).start()
    msg = '{0} started on port {1} with properties {2}.'
    print(msg.format(device.__name__, context.port, properties))
    print('Device access: {}'.format(context.get_device_access()))
    print('Server access: {}'.format(context.get_server_access()))
    context.join()
    print("Done.")


# Main execution
if __name__ == "__main__":
    main()
