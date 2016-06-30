
from ovs33x import OVS33X
from ssh_session import SSHSession

CLASS_MAP = {
    # 'ovs32x': OVS32X,
    '3.3.3': OVS33X,
    # 'ovs34X': OVS34X
}

class OVSFactory(object):
    """Creates an object instance based on OVS version"""
    """Select the class to be instantiated based on OVS version."""
    
    # Decorate 'create' function as a static method (a one that
    # does not require an implicit 'self' as a first argument)
    @staticmethod
    def create(device):
        try:
            session = SSHSession(ip_addr=device['host'],
                                 port=device['port'],
                                 admin_name=device['username'],
                                 admin_pswd=device['password'],
                                 timeout=device['timeout'],
                                 verbose=True)
            session.open()
            cmd = "head -4 /etc/ovs-info\n"
            out = session.execute_command(cmd=cmd, read_delay=10)
            l = out.strip().split()
            release_idx = l.index('release:')
            ovs_version = l[release_idx+1]
            # print "%s" % ovs_version
            session.close()
            # print "%s" % CLASS_MAP[ovs_version]
            return CLASS_MAP[ovs_version](**device)
        except(Exception) as e:
            print "!!!Error: %s\n" % e
            assert(False)
            return None

def ovs_dispatcher(ovs_version):
    """Select the class to be instantiated based on OVS version."""
    return CLASS_MAP[ovs_version]