import json
import time
from ovs.base import OVMServer

class DomainInfo(object):
    def __init__(self, info_sxp):
        self.devices = []
        self.images = []
        assert(isinstance(info_sxp, list))
        self.parse_domain_info(info_sxp)

    def parse_domain_info(self, info_sxp):
        assert(info_sxp[0] == 'domain')
        for (k, v) in info_sxp[1:]:
            if k == 'device':
                device = FactoryDevice.create(v)
                self.devices.append(device)
            elif k == 'image':
                image = Image(v)
                self.images.append(image)
            else:
                setattr(self, k, v)

    def to_json(self):
        """ Returns JSON representation of this object. """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)

    def brief_str(self, indent=0):
        if self.domid == "0":
            return ""
        
        s=("%sDomain Info - %s\n"
           "\n"
           "%sID       : %s\n"
           "%sName     : %s\n"
           "%sPool Name: %s\n"
           "\n"
           "%s%-10s %-10s %-5s %-21s %-20s\n"
           "%s%s %s %s %s %s\n"
           "%s%-10s %-10s %-5s %-21s %-20s"
           ) % \
           (' '*indent, self.name,
            ' '*indent, self.domid,
            ' '*indent, self.name,
            ' '*indent, self.pool_name,
            ' '*indent, "Memory", "Max Memory", "VCPUs",
                        "Total CPU Time (secs)", "Start Time",
            ' '*indent, "-"*10, "-"*10, "-"*5, "-"*21, "-"*20,
            ' '*indent, self.memory, self.maxmem,
                        self.vcpus, self.cpu_time,
                        time.strftime('%m/%d/%Y %H:%M:%S',
                                time.localtime(float(self.start_time)))
            )
           
        dev_str = "\n"
        for device in self.devices:
            dev_str += "\n" + device.brief_str(indent)
            #print("%s" % device.brief_str(indent=4)) 
        
        img_str = ""
        for image in self.images:
            img_str += "\n" + image.brief_str(indent)

        return (s + dev_str + img_str)

    def detailed_str(self):
        pass

class FactoryDevice():
    @staticmethod
    def create(info_sxp):
        if info_sxp[0] == "vif":
            return DeviceVif(info_sxp)
        elif info_sxp[0] == "vfb":
            return DeviceVfb(info_sxp)
        elif info_sxp[0] == "vbd":
            return DeviceVbd(info_sxp)
        elif info_sxp[0] == "console":
            return DeviceConsole(info_sxp)
        else:
            return Device(info_sxp)

class Device(object):
    """ Helper class for 'DomainInfo' class."""
    def __init__(self, info_sxp):
        self.type = None
        self.parse_device_info(info_sxp)

    def parse_device_info(self, info_sxp):
        assert(isinstance(info_sxp, list))
        assert(isinstance(info_sxp[0], basestring))
        self.type = info_sxp[0]
        for (k,v) in info_sxp[1:]:
            setattr(self, k, v)
            
    def brief_str(self, indent=0):
        return ""

    def to_json(self):
        """ Returns JSON representation of this object. """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)

class DeviceVif(Device):
    def __init__(self, info_sxp):
        Device.__init__(self, info_sxp)

    def brief_str(self, indent=0):
        s=("%sDevice: %s\n"
           "%sMAC Address: %s\n"
           "%sBridge Name: %s\n"
           "%sScript: %s\n") % (' '*indent, self.type,
                                  ' '*indent, self.mac,
                                  ' '*indent, self.bridge,
                                  ' '*indent, self.script)
        return s

class DeviceConsole(Device):
    def __init__(self, info_sxp):
        Device.__init__(self, info_sxp)

    def brief_str(self, indent=0):
        s=("%sDevice: %s\n"
           "%sProtocol: %s\n") % (' '*indent, self.type,
                                    ' '*indent, self.protocol)
        return s

class DeviceVbd(Device):
    def __init__(self, info_sxp):
        Device.__init__(self, info_sxp)

    def brief_str(self, indent=0):
        s=("%sDevice: %s\n"
           "%sBootable: %s\n"
           "%sLocation: %s\n") % (' '*indent, self.type,
                                    ' '*indent, self.bootable,
                                    ' '*indent, self.uname)
        return s

class DeviceVfb(Device):
    def __init__(self, info_sxp):
        Device.__init__(self, info_sxp)

    def brief_str(self, indent=0):
        s=("%sDevice: %s\n"
           "%sVNC: %s\n"
           "%sLocation: %s\n") % (' '*indent, self.type,
                                    ' '*indent, self.vnc,
                                    ' '*indent, self.location)
        return s

class Image(object):
    """ Helper class for 'DomainInfo' class."""
    def __init__(self, info_sxp):
        self.parse_image_info(info_sxp)
        # print "Image===> %s" % self.to_json()

    def parse_image_info(self, info_sxp):
        assert(isinstance(info_sxp, list))
        assert(isinstance(info_sxp[0], basestring))
        self.type = info_sxp[0]
        try:
            for item in info_sxp[1:]:
                if len(item) == 2:
                    setattr(self, item[0], item[1])
                elif len(item) > 2:
                    setattr(self, item[0], item[1:])
        except Exception as e:
            print("Error %s" % repr(e))

    def to_json(self):
        """ Returns JSON representation of this object. """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)
    def brief_str(self, indent=0):
        s=("%sImage: %s\n"
           "%sDevice Model: %s\n") % \
            (' '*indent, self.type,
             ' '*indent, self.device_model
            )
            
        """
        s=("%sImage: %s\n"
           "  %sOS Type: %s\n"
           "  %sVGA: %s\n"
           "  %sSerial: %s\n"
           "  %sVNC: %s\n"
           "  %sVNC Listen: %s\n"
            "  %sDevice Model: %s\n"
           "  %sLoader: %s\n") % \
            (' '*indent, self.type,
            ' '*indent, self.guest_os_type,
            ' '*indent, self.stdvga,
            ' '*indent, self.serial,
            ' '*indent, self.vnc,
            ' '*indent, self.vnclisten,
            ' '*indent, self.device_model
            ' '*indent, self.loader)
        """
            
            
           
        return s

