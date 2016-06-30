import json


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
                device = Device(v)
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

class Device(object):
    """ Helper class for 'DomainInfo' class."""
    def __init__(self, info_sxp):
        self.type = None
        self.parse_device_info(info_sxp)
        #print "Device===> %s" % self.to_json()

    def parse_device_info(self, info_sxp):
        assert(isinstance(info_sxp, list))
        assert(isinstance(info_sxp[0], basestring))
        self.type = info_sxp[0]
        for (k,v) in info_sxp[1:]:
            setattr(self, k, v)

    def to_json(self):
        """ Returns JSON representation of this object. """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)

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
