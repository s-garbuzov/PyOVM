
from ovs33x import OVS33X
from utils.ssh_session import SSHSession

OVS_CLASS_MAP = {
    # '3.2.1': OVS32X,
    '3.3.3': OVS33X,
    # '3.4.1': OVS34X
}

class OVSFactory(object):
    """Creates an OVS server object instance based on a server's version"""
    
    # Decorate 'create' function as a static method (a one that
    # does not require an implicit 'self' as a first argument)
    @staticmethod
    def create(device):
        try:
            # Establish SSH session to the destination OVS server
            session = SSHSession(host=device['host'],
                                 port=device['port'],
                                 uname=device['username'],
                                 pswd=device['password'],
                                 timeout=device['timeout'],
                                 verbose=device['verbose'])
            session.open()
            
            # Get OVS server version
            cmd = "head -4 /etc/ovs-info\n"
            out = session.execute_command(cmd=cmd)
            l = out.strip().split()
            version = l[l.index('release:') + 1]
            
            # Given version number instantiate the object
            # representing OVS server
            return OVS_CLASS_MAP[version](session)
        except(Exception) as e:
            print "!!!Error[OVSFactory]: %s\n" % repr(e)
            raise e

def ovs_dispatcher(ovs_version):
    """Select the class to be instantiated based on OVS version."""
    return OVS_CLASS_MAP[ovs_version]