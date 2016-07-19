import time
import json
import xmltodict

from pyovm.utils.xmlrpclib import ServerProxy

class Linux(object):
    def __init__(self, dst):
        self.dst = dst
        self.srv_raw_data = None
        self.server = None
        self.hardware = None

        self.phy_luns = []
        self.scsi_disks = []
        self.scsi_targets = []

        self.mounted_fs = []
        self.repos = {}

        self.pkgs_installed = []
        self.pkgs_updates = []

        self.sys_disk_space = None

        self.boot_time = None

        self.ntp = None

        self.datetime = None
        self.timezone = None
        self.logs = []

        #print("[Linux] %s" % self.uri)
        self.conn = ServerProxy(self.uri, verbose=0)
    
    @property
    def uri(self):
        uri = "https://%s:%s@%s:%s/RPC2" % (self.dst.admin_name,
                                            self.dst.admin_pswd,
                                            self.dst.host,
                                            self.dst.port)
        return uri

    def __xml_postprocessor(self, path, key, value):
        return (key.lower(), value)

    def discover_server(self):
        """'discover_server' RPC"""
        try:
            r = self.conn.discover_server()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], basestring)):
                s='<?xml version'
                if s in r[0]:
                    d = xmltodict.parse(xml_input=r[0],
                                        xml_attribs=True,
                                        process_namespaces=True,
                                        postprocessor=self.__xml_postprocessor)
                    p1 = 'discover_server_result'
                    p2 = 'server'
                    data = d[p1][p2]
                    self.server = Server(data)
                    return self.server
                else:
                    #print json.dumps(d, indent=4)
                    raise Exception("Failed to parse data from response")
            else:
                print json.dumps(r[0], indent=4)
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def discover_hardware(self):
        """'discover_hardware' RPC"""
        try:
            r = self.conn.discover_hardware()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], basestring)):
                s='<?xml version'
                if s in r[0]:
                    d = xmltodict.parse(xml_input=r[0],
                                        xml_attribs=True,
                                        process_namespaces=True,
                                        postprocessor=self.__xml_postprocessor)
                    p1 = 'discover_hardware_result'
                    p2 = 'nodeinformation'
                    data = d[p1][p2]
                    self.hardware = Hardware(data)
                    return self.hardware
                else:
                    #print json.dumps(d, indent=4)
                    raise Exception("Failed to parse data from response")
            else:
                print json.dumps(r[0], indent=4)
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def discover_physical_luns(self):
        """'discover_physical_luns' RPC"""
        try:
            r = self.conn.discover_physical_luns('',)
            assert(isinstance(r, tuple))
            if(isinstance(r[0], basestring)):
                s='<?xml version'
                if s in r[0]:
                    d = xmltodict.parse(xml_input=r[0],
                                        xml_attribs=True,
                                        process_namespaces=True,
                                        postprocessor=self.__xml_postprocessor)
                    p1 = 'discover_physical_luns_result'
                    p2 = 'scsi'
                    p3 = 'disk'
                    data = d[p1]
                    scsi_disk_data = data.get(p2).get(p3)
                    if scsi_disk_data:
                        for item in scsi_disk_data:
                            obj = SCSIDisc(item)
                            self.scsi_disks.append(obj)
                    p4 = 'iscsi_target'
                    scsi_target_data = data.get(p4)
                    if scsi_target_data:
                        for item in scsi_target_data:
                            obj = SCSITarget(item)
                            self.scsi_targets.append(obj)
                    
                            #print json.dumps(item, indent=4)
                else:
                    #print json.dumps(d, indent=4)
                    raise Exception("Failed to parse data from response")
            else:
                print json.dumps(r[0], indent=4)
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def discover_mounted_file_systems(self):
        """'discover_mounted_file_systems' RPC"""
        try:
            r = self.conn.discover_mounted_file_systems("all")
            assert(isinstance(r, tuple))
            if(isinstance(r[0], basestring)):
                s='<?xml version'
                if s in r[0]:
                    d = xmltodict.parse(xml_input=r[0],
                                        xml_attribs=True,
                                        process_namespaces=True,
                                        postprocessor=self.__xml_postprocessor)
                    p1 = 'discover_mounted_file_systems_result'
                    p2 = 'filesystem'
                    data = d[p1][p2]
                    if(isinstance(data, list)):
                        # print json.dumps(data, indent=4)
                        for item in data:
                            fs = MountedFileSystem(item)
                            self.mounted_fs.append(fs)
                        return self.mounted_fs
                    else:
                        raise Exception("Failed to parse data from response")
                else:
                    #print json.dumps(d, indent=4)
                    raise Exception("Failed to parse data from response")
            else:
                print json.dumps(r[0], indent=4)
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def package_get_repositories(self):
        """'package_get_repositories' RPC"""
        try:
            r = self.conn.package_get_repositories()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], dict)):
                self.repos = Repositories(r[0])
                return self.repos
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def package_list(self, scope):
        """'package_list' RPC"""
        assert(scope is 'installed' or scope is 'updates')
        try:
            r = self.conn.package_list(scope)
            assert(isinstance(r, tuple))
            if(isinstance(r[0], list)):
                for e in r[0]:
                    pkg = Package(e)
                    if scope is 'installed':
                        self.pkgs_installed.append(pkg)
                    else:
                        self.pkgs_updates.append(pkg)
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def get_system_disk_space(self):
        """'get_system_disk_space'RPC"""
        try:
            r = self.conn.get_system_disk_space()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], dict)):
                self.sys_disk_space = DiskSpace(r[0])
                return self.sys_disk_space
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def get_last_boot_time(self):
        """'get_last_boot_time' RPC"""
        try:
            r = self.conn.get_last_boot_time()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], dict)):
                self.boot_time = BootTime(r[0])
                return self.boot_time
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def get_ntp(self):
        """'get_ntp' RPC"""
        try:
            r = self.conn.get_ntp()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], list)):
                self.ntp = NTP(r[0])
                return self.ntp
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def get_datetime(self):
        """'get_datetime' RPC"""
        try:
            r = self.conn.get_datetime()
            assert(isinstance(r, tuple))

            if(isinstance(r[0], list)):
                self.datetime = DateTime(r[0])
                return self.datetime
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def get_timezone(self):
        """'get_timezone' RPC"""
        try:
            r = self.conn.get_timezone()
            assert(isinstance(r, tuple))
            if(isinstance(r[0], list)):
                self.timezone = TimeZone(r[0])
                return self.timezone
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def get_log(self, logfile):
        """'get_log' RPC"""
        try:
            r = self.conn.get_log([logfile])
            assert(isinstance(r, tuple))
            #print r[0]
            #print type(r[0])
            if(isinstance(r[0], dict)):
                if(logfile == 'ovs-agent'):
                    log = OVSAgentLog(logfile, r[0][logfile])
                    self.logs.append(log)
                elif(logfile == 'messages'):
                    log = MessagesLog(logfile, r[0][logfile])
                    self.logs.append(log)
                elif(logfile == 'xend'):
                    log = XendLog(logfile, r[0][logfile])
                    self.logs.append(log)
                elif(logfile == 'dmesg'):
                    log = DmesgLog(logfile, r[0][logfile])
                    self.logs.append(log)
                else:
                    raise("Unknown log type '%s'" % logfile)

                return log
            else:
                raise Exception("Failed to parse data from response")
        except Exception as e:
            print("[Linux] Error: %s" % repr(e))

    def to_json(self):
        """ Returns JSON representation of this object. """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)

class Server(Linux):
    """'discover_server' RPC"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

class Hardware(Linux):
    """'discover_hardware' RPC"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

'''
class PhysicalLUNs(Linux):
    """'discover_physical_luns'!!!"""
    def __init__(self):
        self.scsi_disks = []
        pass
'''

class SCSIDisc(Linux):
    """'discover_physical_luns' RPC"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        print self.to_json()

class SCSITarget(Linux):
    """'discover_physical_luns' RPC"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        print self.to_json()

class MountedFileSystem(Linux):
    """'discover_mounted_file_systems' RPC"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

class Repositories(Linux):
    """'package_get_repositories' RPC"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

class Package(Linux):
    """'package_list' RPC"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

class DiskSpace(Linux):
    """'get_system_disk_space' RPC"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

class BootTime(Linux):
    """'get_last_boot_time' RPC"""
    def __init__(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        #print self.to_json()

    def boot_time(self):
        if self.last_boot_time:
            return time.strftime('%m/%d/%Y %H:%M:%S',
                                 time.localtime(float(self.last_boot_time)))

    def current_time(self):
        if self.local_time:
            return time.strftime('%m/%d/%Y %H:%M:%S',
                                 time.localtime(float(self.local_time)))

class NTP(Linux):
    """'get_ntp' RPC"""
    def __init__(self, data):
        self.ntp_servers = data[0]
        self.local_time_source = data[1]
        self.is_ntp_running = data[2]
        #print self.to_json()

class DateTime(Linux):
    """'get_datetime' RPC"""
    def __init__(self, data):
        self.year = data[0]
        self.month = data[1]
        self.date = data[2]
        self.hour = data[3]
        self.min = data[4]
        self.sec = data[5]
        #print self.to_json()

    def to_str(self):
        s = "%s/%s/%s %s:%s:%s" % (self.month, self.date, self.year,
                                   self.hour, self.min, self.sec)
        return s

class TimeZone(Linux):
    """'get_timezone' RPC"""
    def __init__(self, data):
        self.tz = data[0]
        self.utc = data[1]
        
    def to_str(self):
        s = "\"%s\" (\"%s\")" % (self.tz, 'UTC' if self.utc is 'UTC' else 'Local Time')
        return s

class Log(Linux):
    """'get_log' RPC"""
    def __init__(self, filename, logdata):
        self.name = filename
        self.data = logdata

    def to_str(self):
        return str(self.data)

    def errors(self):
        assert(False), "not implemented"

    def warnings(self):
        assert(False), "not implemented"

    def debug(self):
        assert(False), "not implemented"

    def info(self):
        assert(False), "not implemented"

class OVSAgentLog(Log):
    info_pattern = ' INFO '
    dbg_pattern = ' DEBUG '
    warn_pattern = ' WARNING '
    err_pattern = ' ERROR '
    sep = ("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
           "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

    def __init__(self, *args, **kwargs):
        super(OVSAgentLog, self).__init__(*args, **kwargs)
        self.msgs = {self.info_pattern: [],
                     self.dbg_pattern: [],
                     self.warn_pattern: [],
                     self.err_pattern: []
                    }
        slist = self.to_str().split("\n")
        t = []
        msg_type = None
        for s in slist:
            if s.startswith('['):
                if msg_type and t:
                    self.msgs[msg_type].append("\n".join(t))
                    t = []
        
                if s.find(self.info_pattern) != -1:
                    msg_type = self.info_pattern
                elif s.find(self.dbg_pattern) != -1:
                    msg_type = self.dbg_pattern
                elif s.find(self.warn_pattern) != -1:
                    msg_type = self.warn_pattern
                elif s.find(self.err_pattern) != -1:
                    msg_type = self.err_pattern
                else:
                    assert(False)
                    continue
                self.msgs[msg_type].append("%s\n" % s)
            else:
                t.append(s)

    def errors(self):
        s = ""
        for msg in self.msgs[self.err_pattern]:
            if msg.startswith('['):
                s += self.sep
            s += msg
        s += self.sep
        return s

    def warnings(self):
        s = ""
        for msg in self.msgs[self.warn_pattern]:
            if msg.startswith('['):
                s += self.sep
            s += msg
        s += self.sep
        return s

    def debug(self):
        s = ""
        for msg in self.msgs[self.dbg_pattern]:
            if msg.startswith('['):
                s += self.sep
            s += msg
        s += self.sep
        return s
    
    def info(self):
        s = ""
        for msg in self.msgs[self.info_pattern]:
            if msg.startswith('['):
                s += self.sep
            s += msg
        s += self.sep
        return s

class MessagesLog(Log):
    def __init__(self, *args, **kwargs):
        super(MessagesLog, self).__init__(*args, **kwargs)

class DmesgLog(Log):
    def __init__(self, *args, **kwargs):
        super(DmesgLog, self).__init__(*args, **kwargs)

class XendLog(Log):
    def __init__(self, *args, **kwargs):
        super(XendLog, self).__init__(*args, **kwargs)
