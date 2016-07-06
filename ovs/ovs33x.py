
import string
import utils.sxp as sxp

from ovs.base import OVMServer
from domain import DomainInfo
from cluster import ClusterConfigFileInfo, ClusterO2CB
from utils.ssh_session import SSHSession


# Subclass of the  'OVMServer' base class
class OVS33X(OVMServer):
    """Oracle OVS server (release 3.3.X)."""

    def __init__(self, session):
    #def __init__(self, **kwargs):
        """Allocate and return a new instance object."""
        assert(isinstance(session, SSHSession))
        # Invoke the superclass initialization method to initialize
        # inherited attributes
        OVMServer.__init__(self, 'Oracle', 'OVS')
        # Initialize this class attributes
        self._session = session
        self.max_bytes = 9000
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        """
        
        # TODO: need a way to auto-detect 'login prompt' pattern
        #       from the destination host
        self.base_prompt = ("%s@%s" % 
                            (self._session.username, self._session.host))
        #print "^^^^^^ %s" % self.base_prompt

    def to_str(self):
        return ("%s %s:%s" % (self.get_os_type(),
                              self.get_addr, self.get_port))

    def get_addr(self):
        return self.session.host
        # return self.ip_addr

    def get_port(self):
        return self.session.port
        #return self.port

    '''
    def get_firmware_version(self):
        """
        Class specific method that retrieves and returns
        the firmware version from the device.
        """
        pass
    '''
    
    def connected(self):
        return True if(self._session is not None) else False
    
    """
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
    """
    
    def disconnect(self):
        if(self._session is not None):
            self._session.close()

    def strip_command(self, command, output):
        lines = output.split('\n')
        first_line = lines[0]
        if command.strip() in first_line.strip():
            return '\n'.join(lines[1:])
        else:
            return output

    def strip_prompt(self, output):
        lines = output.split('\n')
        last_line = lines[-1]
        if self.base_prompt in last_line:
            return '\n'.join(lines[:-1])
        else:
            return output

    def get_domains_info(self):
        """
        Retrieve from this OVS server all Xen domains information
        and serialize it to internal objects representation.
        NOTE: OVS server returns the data encoded in 'symbolic expression'
              (Lisp programming language notation) format.
        """
        domains = []
        try:
            cmd = "xm list -l\n"
            out = self.execute_command(cmd, 1)
            out = self.strip_command(cmd, out)
            out = self.strip_prompt(out)
            # print out
            info_sxp = sxp.all_from_string(out)
            # print info_sxp
            for dom_info in info_sxp:
                dom = DomainInfo(dom_info)
                domains.append(dom)
                # print "<<<<<<<<<<<<<<<"
                # print dom.to_json()
                # print ">>>>>>>>>>>>>>>"
        except (Exception) as e:
            print("!!!Error: %s" % repr(e))
            raise e

        return domains

    def get_cluster_cfg_info(self):
        cmd = "cat /etc/ocfs2/cluster.conf\n"
        out = self.execute_command(cmd, 1)
        out = self.strip_command(cmd, out)
        out = self.strip_prompt(out)
        cluster = ClusterConfigFileInfo(out)
        return cluster

    def o2cb_list_clusters(self):
        cmd = "o2cb list-clusters\n"
        out = self.execute_command(cmd, 1)
        out = self.strip_command(cmd, out)
        out = self.strip_prompt(out)
        return out

    def o2cb_list_cluster(self, cluster_name):
        cmd = "o2cb list-cluster %s\n" % cluster_name
        out = self.execute_command(cmd, 1)
        out = self.strip_command(cmd, out)
        out = self.strip_prompt(out)
        cluster = ClusterO2CB(out)
        
        return cluster

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

    def get_domains_list(self):
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

    def get_domain_info(self, name):
        """
        Retrieve from this OVS server information about given Xen domain
        and serialize it to internal objects representation.
        NOTE: OVS server returns the data encoded in 'symbolic expression'
              (Lisp programming language notation) format.
        """
        domain = None
        try:
            cmd = "xm list -l %s\n" % name
            out = self.execute_command(cmd, 1)
            out = self.strip_command(cmd, out)
            out = self.strip_prompt(out)
            # print out
            info_sxp = sxp.all_from_string(out)
            domain = DomainInfo(info_sxp[0])
        except (Exception) as e:
            print("!!!Error: %s" % repr(e))
            raise e

        return domain

    def execute_command(self, command, read_delay=.1):
        assert(self._session is not None)
        self._session.send(command)
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
