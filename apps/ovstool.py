#!/usr/bin/env python

"""
command_ssh.py
"""

import json
from ovs.ovs_factory import OVSFactory

# OVS specific info
ovs_info = {
    'host': 'ovs233',
    'port': 22,
    'connection': 'ssh',
    'timeout': 3,
    'username': 'root',
    'password': 'oracle',
    'max_bytes': 9000,
    'verbose': True
}


def show_domain(ovs_info, name):
    try:
        ovs = OVSFactory.create(ovs_info)
        ovs.connect()
        if(ovs.connected()):
            domain = ovs.get_domain(name)
            
            ovs.disconnect()
    except(Exception) as e:
        print "!!!Error: %s\n" % repr(e)
        assert(False)
        return None
    pass


def show_domains(ovs_info):
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
        assert(False)
        return None

def tmp():
    s="""
(domain
    (domid 11)
    (cpu_weight 27500)
    (cpu_cap 0)
    (pool_name Pool-0)
    (bootloader '')
    (vcpus 1)
    (cpus (()))
    (on_poweroff destroy)
    (description '')
    (on_crash restart)
    (uuid 0004fb00-0006-0000-7c52-2c7d71072a52)
    (bootloader_args '')
    (name 0004fb00000600007c522c7d71072a52)
    (on_reboot restart)
    (maxmem 1032)
    (memory 1030)
    (shadow_memory 10)
    (features '')
    (on_xend_start ignore)
    (on_xend_stop ignore)
    (start_time 1467122071.27)
    (cpu_time 3232.65829106)
    (online_vcpus 1)
    (image
        (hvm
            (kernel '')
            (expose_host_uuid 0)
            (superpages 0)
            (videoram 4)
            (hpet 0)
            (stdvga 0)
            (vnclisten 127.0.0.1)
            (loader /usr/lib/xen/boot/hvmloader)
            (xen_platform_pci 1)
            (nestedhvm 0)
            (rtc_timeoffset 0)
            (pci ())
            (hap 1)
            (localtime 0)
            (timer_mode 1)
            (pci_msitranslate 1)
            (oos 1)
            (apic 1)
            (usbdevice tablet)
            (vpt_align 1)
            (serial pty)
            (vncunused 1)
            (boot c)
            (pae 1)
            (viridian 0)
            (acpi 1)
            (vnc 1)
            (nographic 0)
            (nomigrate 0)
            (usb 0)
            (tsc_mode 0)
            (guest_os_type linux)
            (device_model /usr/lib/xen/bin/qemu-dm)
            (keymap en-us)
            (pci_power_mgmt 0)
            (xauthority /root/.Xauthority)
            (isa 0)
            (notes (SUSPEND_CANCEL 1))
        )
    )
    (status 2)
    (state -b----)
    (store_mfn 1044476)
    (device
        (vif
            (bridge 10e69b4de3)
            (mac 00:21:f6:00:08:b5)
            (script /etc/xen/scripts/vif-bridge)
            (uuid f626bd18-778d-c3af-526d-87ba2fefaa0a)
            (backend 0)
        )
    )
    (device
        (console
            (protocol vt100)
            (location 4)
            (uuid 74f35192-5b9b-6927-eaa5-bf9f03475778)
        )
    )
    (device
        (vbd
            (protocol x86_64-abi)
            (uuid e96afe78-957b-c0d2-832c-02769d9726c3)
            (bootable 1)
            (dev xvda:disk)
            (uname
                file:/OVS/Repositories/0004fb00000300002160f6433014d23a/VirtualDisks/0004fb00001200006a75694a0a25bea8.img
            )
            (mode w)
            (discard-enable 0)
            (backend 0)
            (VDI '')
        )
    )
    (device
        (vfb
            (vncunused 1)
            (vnc 1)
            (uuid eabb9937-6700-ffab-33ab-be62cb608aa1)
            (vnclisten 127.0.0.1)
            (keymap en-us)
            (location 127.0.0.1:5901)
        )
    )
)
    """
    import re
    #s1 = s.replace("\n", "").lstrip().rstrip()
    #print s1
    #s1 = s.replace("\n", "")
    #s2 = re.sub(' +',' ',s1)
    #print s2.replace(' ', ':')
    #s1 = re.sub(' +',' ',s)
    #print s1
    #s1 = s.replace('(', '{').replace(')', '}')
    #s2 = re.sub(r'([^\s])\s([^\s])', r'\1:\2',s1)
    #print s2
    #print s
    
    t1="""
    (device
        (vif
            (bridge 10e69b4de3)
            (mac 00:21:f6:00:08:b5)
            (script /etc/xen/scripts/vif-bridge)
            (uuid f626bd18-778d-c3af-526d-87ba2fefaa0a)
            (backend 0)
        )
    )
    """
    t2 = t1.replace("\n", "")
    print t2
    #t3 = re.sub(r'([^\s])\s([^\s])', r'\1:\2',t2)
    t3 = re.sub(' +',' ',t2)
    print t3
    
    """
    import re
    d = dict(re.findall(r"\((\S+)\s+\(*(.*?)\)+",s))
    //print s
    for k,v in d.items():
        print "%s: %s" % (k, v)
    """
    
    '''
    x="{key1 value1} {key2 value2} {key3 {value with spaces}}"
    print dict(re.findall(r"\{(\S+)\s+\{*(.*?)\}+",x))
    
    
    
    print s.strip()
    l = s.strip().split('\n')
    t = json.loads(s)
    print t
    '''
    
    
    
    
    #for i, j in enumerate(l):
    #    print "=> i=%s, j=%s" % (i,j)
    
    # print s.replace(" ", ":")
    #rows = ( line.split() for line in s )
    #print type(rows)
    #for row in rows:
    #    print row
    
    
    

def main():
    tmp()
    return
    
    # show_domain(ovs_info, "0004fb0000060000236e45007b980aa1")
    # return
    
    
    show_domains(ovs_info)

if __name__ == '__main__':
    main()
    
