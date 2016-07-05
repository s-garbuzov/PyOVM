#!/usr/bin/env python

"""
command_ssh.py
"""

import json
from ovs.factory import OVSFactory

# OVS specific info
server = {
    'host': 'ovs233',
    'connection': 'ssh',
    'port': 22,
    'timeout': 3,
    'username': 'root',
    'password': 'oracle',
    'verbose': False
}


def show_domain_info(server, dom_name):
    debug = False
    try:
        ovs = OVSFactory.create(server)
        #ovs.connect()
        if(ovs.connected()):
            dom = ovs.get_domain_info(dom_name)
            if debug:
                print dom.to_json()
            else:
                print("\n").strip()
                print(" OVS Server '%s'\n" % server['host'])
                print("   Domain Info - %s\n" % dom.name)
                print("     ID       : %s" % dom.domid)
                print("     Name     : %s" % dom.name)
                print("     Pool Name: %s" % dom.pool_name)
                
                print("\n").strip()
                print("     %-10s %-10s %-5s %-20s %-20s" %
                      ("Memory", "Max Memory", "VCPUs",
                       "CPU Time", "Start Time"))
                print("     %s %s %s %s %s" %
                      ("-"*10, "-"*10, "-"*5, "-"*20, "-"*20))
                print("     %-10s %-10s %-5s %-20s %-20s" %
                      (dom.memory, dom.maxmem,
                       dom.vcpus, dom.cpu_time, dom.start_time))
                print("\n").strip()
                
                devices = dom.devices
                for device in devices:
                    print("%s" % device.brief_str(indent=4)) 
                
                images = dom.images
                for image in images:
                    print("%s" % image.brief_str(indent=4))

            ovs.disconnect()
    except(Exception) as e:
        print "!!!Error[show_domain]: %s\n" % repr(e)
        raise e

def show_domains_info(server):
    debug = False
    try:
        ovs = OVSFactory.create(server)
        # ovs.connect()
        if(ovs.connected()):
            domains = ovs.get_domains_info()
            # print type(domains)
            if debug:
                for dom in domains:
                    print "<<<<<<<<<<<<<<<"
                    print dom.to_json()
                    print ">>>>>>>>>>>>>>>"
            else:
                print("\n").strip()
                print(" OVS Server '%s'\n" % server['host'])
                print("   Domains Info\n")
                print("    %-3s %-32s %-6s %-5s %-10s" %
                      ("ID", "Name", "Memory", "VCPUs", "Time"))
                print("    %s %s %s %s %s" %
                      ("-"*3, "-"*32, "-"*6, "-"*5, "-"*15))
                for dom in domains:
                    print("    %-3s %-32s %-6s %-5s %-10s" %
                          (dom.domid, dom.name,
                           dom.memory, dom.vcpus, dom.cpu_time))
                print("\n")

            ovs.disconnect()
    except(Exception) as e:
        print "!!!Error: %s\n" % repr(e)
        raise e
        #assert(False)
        return None

def show_domains_list(server):
    try:
        ovs = OVSFactory.create(server)
        # ovs.connect()
        if(ovs.connected()):
            domains = ovs.get_domains()

            print("\n").strip()
            print(" Domains Info (%s) \n" % server['host'])
            print("  %-3s %-32s %-6s %-5s %-10s" %
                  ("ID", "Name", "Memory", "VCPUs", "Time"))
            print("  %s %s %s %s %s" % ("-"*3, "-"*32, "-"*6, "-"*5, "-"*10))
            for dom in domains:
                print("  %-3s %-32s %-6s %-5s %-10s" %
                      (dom.id, dom.name, dom.mem, dom.vcpus, dom.time))
            print("\n")

            ovs.disconnect()
    except(Exception) as e:
        print "!!!Error: %s\n" % repr(e)
        raise e

def show_cluster_cfg(server):
    try:
        ovs = OVSFactory.create(server)
        # ovs.connect()
        if(ovs.connected()):
            cfg = ovs.get_cluster_cfg_info()
            # print "!!! cluster_cfg=%s" % cfg.to_json()
            print("\n").strip()
            print(" OVS Server '%s'\n" % server['host'])
            print("   Cluster Configuration Info")
            names = cfg.get_cluster_names()
            for name in names:
                print("\n").strip()
                print("    Cluster '%s'\n" % name)
                print("       Nodes Count: %s" % cfg.get_node_count(name))
                print("       Heartbeat Mode: %s" % cfg.get_hb_mode(name))
                print("\n").strip()
                print("       Nodes\n")
                nodes = cfg.get_nodes(name)
                for node in nodes:
                    print("         Name: %s" % node['name'])
                    print("         Number: %s" % node['number'])
                    print("         IPv4 Address: %s" % node['ip_address'])
                    print("         IPv4 Port: %s" % node['ip_port'])
                    print("\n").strip()
                    
                print("       Heartbeats\n")
                hbs = cfg.get_heartbeats(name)
                for hb in hbs:
                    print("         Region UUID: %s" % hb['region'])

                print("\n").strip()

            ovs.disconnect()
    except(Exception) as e:
        print "!!!Error: %s\n" % repr(e)
        raise e
    pass

def main():
    show_cluster_cfg(server)
    #show_domains_info(server)
    #show_domain_info(server, "0004fb00000600007c522c7d71072a52")
    # return
    pass
    
    
    # show_domains_list(ovs_info)

if __name__ == '__main__':
    main()
    
