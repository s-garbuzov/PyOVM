#!/usr/bin/env python

"""
command_ssh.py
"""

import json
from ovs.factory import OVSFactory

# OVS specific info
ovs_info = {
    'host': 'ovs233',
    'connection': 'ssh',
    'port': 22,
    'timeout': 3,
    'username': 'root',
    'password': 'oracle',
    'verbose': True
}


def show_domain(ovs_info, name):
    debug = False
    try:
        ovs = OVSFactory.create(ovs_info)
        #ovs.connect()
        if(ovs.connected()):
            dom = ovs.get_domain_info(name)
            if debug:
                print dom.to_json()
            else:
                print("\n").strip()
                print(" OVS Server '%s'\n" % ovs_info['host'])
                print("  Domain Info\n")
                print("   %-3s %-32s %-6s %-5s %-10s" %
                      ("ID", "Name", "Memory", "VCPUs", "Time"))
                print("   %s %s %s %s %s" %
                      ("-"*3, "-"*32, "-"*6, "-"*5, "-"*10))
                print("   %-3s %-32s %-6s %-5s %-10s" %
                      (dom.domid, dom.name,
                       dom.memory, dom.vcpus, dom.cpu_time))
                print("\n")
            ovs.disconnect()
    except(Exception) as e:
        print "!!!Error[show_domain]: %s\n" % repr(e)
        raise e

def show_domains_info(ovs_info):
    debug = False
    try:
        ovs = OVSFactory.create(ovs_info)
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
                print(" OVS Server '%s'\n" % ovs_info['host'])
                print("  Domains Info\n")
                print("   %-3s %-32s %-6s %-5s %-10s" %
                      ("ID", "Name", "Memory", "VCPUs", "Time"))
                print("   %s %s %s %s %s" %
                      ("-"*3, "-"*32, "-"*6, "-"*5, "-"*15))
                for dom in domains:
                    print("   %-3s %-32s %-6s %-5s %-10s" %
                          (dom.domid, dom.name,
                           dom.memory, dom.vcpus, dom.cpu_time))
                print("\n")

            ovs.disconnect()
    except(Exception) as e:
        print "!!!Error: %s\n" % repr(e)
        raise e
        #assert(False)
        return None



def show_domains_list(ovs_info):
    try:
        ovs = OVSFactory.create(ovs_info)
        ovs.connect()
        if(ovs.connected()):
            domains = ovs.get_domains()

            print("\n").strip()
            print(" Domains Info (%s) \n" % ovs_info['host'])
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

def main():
    show_domains_info(ovs_info)
    show_domain(ovs_info, "0004fb00000600007c522c7d71072a52")
    # return
    
    
    # show_domains_list(ovs_info)

if __name__ == '__main__':
    main()
    
