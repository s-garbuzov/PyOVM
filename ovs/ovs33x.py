
from ovs import OVMServer
from ssh_session import SSHSession

# Subclass of the 'NetworkDevice' base class
class OVS33X(OVMServer):
    """Cisco IOS-XR device with device specific methods."""

    def __init__(self, **kwargs):
        """Allocate and return a new instance object."""

        # Invoke the superclass initialization method to initialize
        # inherited attributes
        OVMServer.__init__(self, 'Oracle', 'OVS')
        # Initialize this class attributes
        self._session = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_str(self):
        return "%s %s:%s" % (self.get_os_type(), self.ip_addr, self.port)

    def get_addr(self):
        return self.ip_addr

    def get_port(self):
        return self.port

    def get_firmware_version(self):
        """
        Class specific method that retrieves and returns
        the firmware version from the device.
        """
        pass

    def connected(self):
        return True if(self._session is not None) else False

    def connect(self):
        if(self._session is not None):
            return self._session

        if(self.connection == 'ssh'):
            session = SSHSession(self.host, self.port,
                                 self.username, self.password,
                                 self.max_bytes,
                                 self.timeout, self.verbose)
        else:
            assert False, 'unexpected attribute value: %s' % self.channel

        if(session.open() is not None):
            self._session = session
        return self._session

    def disconnect(self):
        if(self._session is not None):
            self._session.close()

    def enable_privileged_commands(self):
        assert(self._session is not None)
        cmd = "enable\n"
        self._session.send(cmd)
        output = self._session.recv(read_delay=1)
        if(self.password_prompt in output):
            password = "%s\n" % self.password
            self._session.send(password)
            output = self._session.recv(read_delay=1)

    def disable_paging(self):
        assert(self._session is not None)
        cmd = 'terminal length 0\n'
        self.execute_command(cmd, 1)

    def check_cfg_mode(self):
        assert(self._session is not None)
        cmd = '\n'
        output = self.execute_command(cmd, 1)
        config_prompt = "(%s)%s" % ('config', self.admin_prompt)
        if(config_prompt in output):
            return True
        else:
            return False

    def enter_cfg_mode(self):
        assert(self._session is not None)
        if not self.check_cfg_mode():
            cmd = "configure terminal\n"
            self.execute_command(cmd, 1)

    def get_domains(self):
        res = []
        cmd = "xl list\n"
        out = self.execute_command(cmd)
        lines = out.split("\n")
        last_idx = len(lines) -1
        for idx, line in enumerate(lines):
            if idx == 0 or idx == 1 or idx == last_idx:
                continue
            res.append(Domain(line))
        return res


    def get_domain(self, name):
        res = []
        cmd = "xm list -l %s\n" % name
        out = self.execute_command(cmd)
        lines = out.split("\n")
        last_idx = len(lines) -1
        for idx, line in enumerate(lines):
            if idx == 0 or idx == last_idx:
                continue
            #res.append(line)
            print line
        # print res
        """
        lines = out.split("\n")
        last_idx = len(lines) -1
        for idx, line in enumerate(lines):
            if idx == 0 or idx == 1 or idx == last_idx:
                continue
            res.append(Domain(line))
        return res
        """
        

    def execute_command(self, command, read_delay=.1):
        assert(self._session is not None)
        self._session.send(command)
        # print ("1)+++++++++")
        output = self._session.recv(read_delay)
        return output


class Domain(object):
    def __init__(self, s):
        self.str = s
        l = s.split()
        self.name = l[0] if l[0] else None
        self.id = l[1] if l[1] else None
        self.mem = l[2] if l[2] else None
        self.vcpus = l[3] if l[3] else None
        self.state = l[4] if l[4] else None
        self.time = l[5] if l[5] else None

    def do_print(self):
        pass
    """
    def to_dict(self):
        d = {'name': "", 'id': "", 'mem': "", 'vcpus': "", 'state'}
        print "Domain=> %s" % self.str
    """




