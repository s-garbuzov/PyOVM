
class Linux(object):
    def __init__(self, dst):
        s = "https://%s:%s@%s/RPC2" % (dst.name, dst.pswd, dst.host, dst.port)
        #self.uri = "https://%s:%s@%s" % ("oracle", "oracle", "ovs240:8899/RPC2")
        print("[Linus] %s" % s)
        pass
    