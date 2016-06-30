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

    def __init__(self, ip_addr, port,
                 admin_name, admin_pswd,
                 max_bytes=9000,
                 timeout=None, verbose=False):
        self._session = None
        self._remote_shell = None
        self._max_bytes = max_bytes
        self.ip_addr = ip_addr
        self.port = port
        self.admin_name = admin_name
        self.admin_pswd = admin_pswd
        self.timeout = timeout
        self.verbose = verbose

    def open(self):
        if(self._session is not None):
            return self._session

        try:
            client = SSH2.SSHClient()
            client.set_missing_host_key_policy(SSH2.AutoAddPolicy())
            if(self.verbose):
                print("Connecting to %s:%s" % (self.ip_addr, self.port))
            client.connect(hostname=self.ip_addr, port=self.port,
                           username=self.admin_name,
                           password=self.admin_pswd,
                           look_for_keys=False, allow_agent=False,
                           timeout=self.timeout)
            self._session = client
            self._remote_shell = client.invoke_shell()
            if(self.verbose):
                print("Connection to %s:%s has been established" %
                      (self.ip_addr, self.port))
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
                          (self.ip_addr, self.port))
            except (Exception) as e:
                print "!!!Error, %s " % e

    def send(self, data):
        assert(self._remote_shell is not None)
        self._remote_shell.send(data)

    def recv(self, read_delay=.1):
        assert(self._remote_shell is not None)
        if self.wait_for_recv_ready(read_delay):
            return self._remote_shell.recv(self._max_bytes)
        return ""

    def wait_for_recv_ready(self, read_delay=.1):
        """Wait until data is ready to be read (is buffered)."""
        i = 0
        max_loops=100
        while i <= max_loops:
            if self._remote_shell.recv_ready():
                # print ("2)+++++++++")
                return True
            else:
                i += 1
            time.sleep(.5)
        raise Exception("Timed out waiting for recv_ready.")

    def execute_command(self, cmd, read_delay=1):
        assert(self._session is not None)
        assert(self._remote_shell is not None)
        self.send(cmd)
        return self.recv(read_delay)
