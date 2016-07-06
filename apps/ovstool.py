#!/usr/bin/env python

"""
command_ssh.py
"""

import time
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
                print("     %-10s %-10s %-5s %-21s %-20s" %
                      ("Memory", "Max Memory", "VCPUs",
                       "Total CPU Time (secs)", "Start Time"))
                print("     %s %s %s %s %s" %
                      ("-"*10, "-"*10, "-"*5, "-"*21, "-"*20))
                print("     %-10s %-10s %-5s %-21s %-20s" %
                      (dom.memory, dom.maxmem,
                       dom.vcpus, dom.cpu_time,
                       time.strftime('%m/%d/%Y %H:%M:%S',
                                     time.localtime(float(dom.start_time)))))
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

def show_domains_info(server, brief=True):
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
                      ("ID", "Name", "Memory", "VCPUs", "Total CPU Time (secs)"))
                print("    %s %s %s %s %s" %
                      ("-"*3, "-"*32, "-"*6, "-"*5, "-"*21))
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
        if(ovs.connected()):
            cluster_cfg_info = ovs.get_cluster_cfg_info()
            # print "!!! cluster_cfg=%s" % cfg.to_json()
            print("\n").strip()
            print(" OVS Server '%s'\n" % server['host'])
            print("   Cluster Configuration Info")
            names = cluster_cfg_info.get_cluster_names()
            for name in names:
                print("\n").strip()
                print("    Cluster '%s'\n" % name)
                print("       Nodes Count: %s" %
                       cluster_cfg_info.get_node_count(name))
                print("       Heartbeat Mode: %s" % 
                      cluster_cfg_info.get_hb_mode(name))
                print("\n").strip()

                print("%-11s %-16s %-15s %-10s" %
                      ("       Node Number", "Node Name",
                       "IPv4 Address", "IPv4 Port"))
                print("       %s %s %s %s" %
                      ("-"*11, "-"*16, "-"*15, "-"*10))
                nodes = cluster_cfg_info.get_nodes(name)
                for node in nodes:
                    print("       %-11s %-16s %-15s %-10s" %
                          (node['number'], node['name'],
                           node['ip_address'], node['ip_port']))
                print("\n").strip()
                print("       %-52s" % ("Heartbeat Region UUID"))
                print("       %s" % ("-"*52))
                hbs = cluster_cfg_info.get_heartbeats(name)
                for hb in hbs:
                    print("       %-52s" % hb['region'])

                print("\n").strip()

            ovs.disconnect()
    except(Exception) as e:
        print "!!!Error: %s\n" % repr(e)
        raise e

def show_cluster_names(server):
    try:
        ovs = OVSFactory.create(server)
        if(ovs.connected()):
            l = ovs.o2cb_list_clusters()
            print l
            
            ovs.disconnect()
    except(Exception) as e:
        print "!!!Error: %s\n" % repr(e)
        raise e

def show_o2cb_clusters(server):
    try:
        ovs = OVSFactory.create(server)
        if(ovs.connected()):
            names = ovs.o2cb_list_clusters().split("\n")
            print("\n").strip()
            print(" OVS Server '%s'\n" % server['host'])
            print("   O2CB Clusters Info")
            for name in names:
                #print name
                cluster = ovs.o2cb_list_cluster(name)
                
                print("\n").strip()
                print("     Cluster '%s'\n" % name)
                print("       Nodes Count: %s" %
                       cluster.cluster['node_count'])
                print("       Heartbeat Mode: %s" % 
                      cluster.cluster['heartbeat_mode'])
                print("\n").strip()

                print("%-11s %-16s %-15s %-10s" %
                      ("       Node Number", "Node Name",
                       "IP Address", "Port"))
                print("       %s %s %s %s" %
                      ("-"*11, "-"*16, "-"*15, "-"*10))
                for node in cluster.nodes:
                    print("       %-11s %-16s %-15s %-10s" %
                          (node['number'], node['name'],
                           node['ip_address'], node['ip_port']))
                print("\n").strip()
                print("       %-52s" % ("Heartbeat Region UUID"))
                print("       %s" % ("-"*52))
                for hb in cluster.heartbeats:
                    print("       %-52s" % hb['region'])

                print("\n").strip()

            ovs.disconnect()
    except(Exception) as e:
        print "!!!Error: %s\n" % repr(e)
        raise e

def show_o2cb_cluster(server, cluster_name):
    try:
        ovs = OVSFactory.create(server)
        if(ovs.connected()):
            cluster = ovs.o2cb_list_cluster(cluster_name)
            print("\n").strip()
            print(" OVS Server '%s'\n" % server['host'])
            #print("\n").strip()
            print("   Cluster '%s'\n" % cluster_name)
            print("     Nodes Count: %s" %
                   cluster.cluster['node_count'])
            print("     Heartbeat Mode: %s" % 
                  cluster.cluster['heartbeat_mode'])
            print("\n").strip()

            print("%-11s %-16s %-15s %-10s" %
                  ("     Node Number", "Node Name",
                   "IP Address", "Port"))
            print("     %s %s %s %s" %
                  ("-"*11, "-"*16, "-"*15, "-"*10))
            for node in cluster.nodes:
                print("     %-11s %-16s %-15s %-10s" %
                      (node['number'], node['name'],
                       node['ip_address'], node['ip_port']))
            print("\n").strip()
            print("     %-52s" % ("Heartbeat Region UUID"))
            print("     %s" % ("-"*52))
            for hb in cluster.heartbeats:
                print("     %-52s" % hb['region'])

            print("\n").strip()
            
            ovs.disconnect()
    except(Exception) as e:
        print "!!!Error: %s\n" % repr(e)
        raise e

def main():
    #show_cluster_names(server)
    #show_cluster_cfg(server)
    #show_o2cb_clusters(server)
    #show_o2cb_cluster(server, "1b277644540ad2d6")
    show_domains_info(server)
    # show_domain_info(server, "0004fb00000600007c522c7d71072a52")
    # return
    
    
    # show_domains_list(ovs_info)

if __name__ == '__main__':
    main()
    
