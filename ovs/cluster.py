import string
import json

class ClusterConfigInfo(object):
    def __init__(self, cfg_info):
        assert(isinstance(cfg_info, basestring))
        self.clusters = []
        self.heartbeats = []
        self.nodes = []
        self.parse_config_info(cfg_info)

    def parse_config_info(self, cfg_info):
        #print cfg_info
        lines = cfg_info.split("\n")
        # print lines
        for line in lines:
            #line = line.split('#')[0].strip()
            if not line:
                continue
            elif line.startswith('node:'):
                d = {}
                self.nodes.append(d)
            elif line.startswith('cluster:'):
                d = {}
                self.clusters.append(d)
            elif line.startswith('heartbeat:'):
                d = {}
                self.heartbeats.append(d)
            else:
                parts = map(string.strip, line.split('='))
                if len(parts) == 2 and parts[0]:
                    d[parts[0]] = parts[1]

    def get_cluster_names(self):
        names = []
        for item in self.clusters:
            names.append(item['name'])
        return names

    def get_node_count(self, cluster_name):
        for item in self.clusters:
            if item['name'] == cluster_name:
                return item['node_count']
        
    def get_hb_mode(self, cluster_name):
        for item in self.clusters:
            if item['name'] == cluster_name:
                return item['heartbeat_mode']

    def get_nodes(self, cluster_name):
        nodes = []
        for item in self.nodes:
            if item['cluster'] == cluster_name:
                nodes.append(item)
        return nodes

    def get_heartbeats(self, cluster_name):
        hbs = []
        for item in self.heartbeats:
            if item['cluster'] == cluster_name:
                hbs.append(item)
        return hbs

    def to_json(self):
        """ Returns JSON representation of this object. """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)

