"""Contain the context to run a device without a database."""

# Imports
from socket import socket
from functools import wraps
from time import sleep, time
from threading import Thread
from PyTango.server import run
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
                try:
                    return func(*args, **kwargs)
                except errors as e:
                    sleep(pause)
                    first = False
            raise e
        return wrapper
    return dec

# Get available port
def get_port():
    sock = socket()
    sock.bind(('',0))
    return sock.getsockname()[1]


# No database Tango context
class NodbTangoContext(object):
    """ Context to run a device without a database."""

    nodb = "#dbase=no"
    command = "{} {} -ORBendPoint giop:tcp::{} -file={}"
    connect_time = 1.0

    def __init__(self, device_cls, server=None, instance=None, device=None,
                 properties={}, db="tango.db", port=0):
        """Inititalize the context to run a given device."""
        # Argument
        tangoclass = device_cls.__name__
        if not server: server = tangoclass
        if not instance: instance = server.lower()
        if not device: device = 'test/nodb/' + server.lower()
        if not port: port = get_port()
        # Attributes
        self.port = port
        self.device_name = device
        self.server_name = "/".join(("dserver", server, instance))
        self.host = "localhost:{}/".format(self.port)
        self.device = self.server = None
        # File
        self.generate_db_file(server, instance, device,
                                        tangoclass, properties, db)
        # Thread
        string = self.command.format(server, instance, port, db)
        args = ((device_cls,), string.split())
        self.thread = Thread(target=run, args=args)

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

