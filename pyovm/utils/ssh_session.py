"""
Class that handles SSH connection to a network device.
Defines methods that are generally applicable to different platforms.
"""


# built-in modules
import socket
import time

# third-party modules
import paramiko as SSH2


class SSHSession(object):
    """SSH connection to a remote device."""

    def __init__(self, host, port,
                 uname, pswd,
                 max_bytes=9000,
                 timeout=None, verbose=False):
        self._session = None
        self._remote_shell = None
        self._max_bytes = max_bytes
        self.host = host
        self.port = port
        self.username = uname
        self.password = pswd
        self.timeout = timeout
        self.verbose = verbose

    def open(self):
        if(self._session is not None):
            return self._session

        try:
            client = SSH2.SSHClient()
            client.set_missing_host_key_policy(SSH2.AutoAddPolicy())
            if(self.verbose):
                print("Connecting to %s:%s" % (self.host, self.port))
            client.connect(hostname=self.host, port=self.port,
                           username=self.username,
                           password=self.password,
                           look_for_keys=False, allow_agent=False,
                           timeout=self.timeout)
            self._session = client
            self._remote_shell = client.invoke_shell()
            if(self.verbose):
                print("Connection to %s:%s has been established" %
                      (self.host, self.port))
            # flush read buffer from unwanted data
            self.recv(0)
            return self._session
        except (SSH2.BadHostKeyException,
                SSH2.AuthenticationException,
                SSH2.SSHException,
                socket.error) as e:
            print "!!!Error: %s " % e
            return None

    def close(self):
        assert(self._session is not None)
        if self._session is not None:
            try:
                self._session.close()
                if(self.verbose):
                    print("Connection to %s:%s has been closed" %
                          (self.host, self.port))
            except (Exception) as e:
                print "!!!Error, %s " % e

    def send(self, data):
        assert(self._remote_shell is not None)
        self._remote_shell.send(data)

    def recv(self, read_delay=.1):
        assert(self._remote_shell is not None)
        if self.wait_for_recv_ready(read_delay):
            out = self._remote_shell.recv(self._max_bytes)
            return out
        return ""

    def wait_for_recv_ready(self, read_delay=.5):
        """Wait until data is ready to be read (is buffered)."""
        i = 0
        max_loops=100
        # max_loops = read_delay * 2
        time.sleep(read_delay)
        while i <= max_loops:
            if self._remote_shell.recv_ready():
                return True
            else:
                i += 1
            time.sleep(.1)
        raise Exception("Timed out waiting for recv_ready.")

    def execute_command(self, cmd, read_delay=.5):
        assert(self._session is not None)
        assert(self._remote_shell is not None)
        self.send(cmd)
        out = self.recv(read_delay)
        return out
