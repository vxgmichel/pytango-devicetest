"""Contain the context to run a device without a database."""

# Imports
from socket import socket
from functools import wraps
from time import sleep, time
from threading import Thread


# PyTango imports
try:
    from PyTango.server import run
except ImportError:
    from PyTango.server import server_run as run
from PyTango import DeviceProxy, Database, ConnectionFailed


# Retry decorator
def retry(period, errors, pause=0.001):
    """Retry decorator."""
    errors = tuple(errors)

    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            stop = time() + period
            first = True
            while first or time() < stop:
                sleep(pause)
                try:
                    return func(*args, **kwargs)
                except errors as e:
                    first = False
            raise e
        return wrapper
    return dec


# Get available port
def get_port():
    sock = socket()
    sock.bind(('', 0))
    res = sock.getsockname()[1]
    del sock
    return res


# No database Tango context
class TangoTestContext(object):
    """ Context to run a device without a database."""

    nodb = "#dbase=no"
    command = "{0} {1} -ORBendPoint giop:tcp::{2} -file={3}"
    connect_time = 3.0

    def __init__(self, device, device_cls=None, server_name=None,
                 instance_name=None, device_name=None, properties={},
                 db="tango.db", port=0, debug=0, daemon=False):
        """Inititalize the context to run a given device."""
        # Argument
        tangoclass = device.__name__
        if not server_name:
            server_name = tangoclass
        if not instance_name:
            instance_name = server_name.lower()
        if not device_name:
            device_name = 'test/nodb/' + server_name.lower()
        if not port:
            port = get_port()
        # Attributes
        self.port = port
        self.device_name = device_name
        self.server_name = "/".join(("dserver", server_name, instance_name))
        self.host = "localhost:{0}/".format(self.port)
        self.device = self.server = None
        # File
        self.generate_db_file(server_name, instance_name, device_name,
                              tangoclass, properties, db)
        # Tango classes
        if device_cls:
            classes = {tangoclass: (device_cls, device)}
        else:
            classes = (device,)
        # Thread
        string = self.command.format(server_name, instance_name, port, db)
        string += " -v{0}".format(debug) if debug else ""
        args = (classes, string.split())
        self.thread = Thread(target=run, args=args)
        self.thread.daemon = daemon

    @staticmethod
    def generate_db_file(server, instance, device,
                         tangoclass=None, properties={}, db="tango.db"):
        """Generate a database file corresponding to the given arguments."""
        if not tangoclass:
            tangoclass = server
        with open(db, 'w') as f:
            f.write("/".join((server, instance, "DEVICE", tangoclass)))
            f.write(': "' + device + '"\n')
        db = Database(db)
        db.put_device_property(device, properties)
        return db

    def get_device_access(self):
        """Return the full device name."""
        return self.host+self.device_name+self.nodb

    def get_server_access(self):
        """Return the full server name."""
        return self.host+self.server_name+self.nodb

    def start(self):
        """Run the server."""
        self.thread.start()
        self.connect()
        return self

    @retry(connect_time, [ConnectionFailed])
    def connect(self):
        self.device = DeviceProxy(self.get_device_access())
        self.server = DeviceProxy(self.get_server_access())

    def stop(self, timeout=None):
        """Kill the server."""
        if self.server:
            self.server.Kill()
        self.thread.join(timeout)

    def join(self, timeout=None):
        self.thread.join(timeout)

    def __enter__(self):
        """Enter method for context support."""
        if not self.thread.isAlive():
            self.start()
        return self.device

    def __exit__(self, exc_type, exception, trace):
        """Exit method for context support."""
        self.stop()
