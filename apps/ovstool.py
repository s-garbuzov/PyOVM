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
    'verbose': False
}


def show_domain_info(ovs_info, name):
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
    #show_domains_info(ovs_info)
    show_domain_info(ovs_info, "0004fb00000600007c522c7d71072a52")
    # return
    
    
    # show_domains_list(ovs_info)

if __name__ == '__main__':
    main()
    
