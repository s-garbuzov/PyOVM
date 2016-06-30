
import json
import ovs.sxp as sxp



s="""
(domain
    (domid 1)
    (cpu_weight 27500)
    (cpu_cap 0)
    (pool_name Pool-0)
    (bootloader /usr/bin/pygrub)
    (vcpus 2)
    (cpus (() ()))
    (on_poweroff destroy)
    (description '')
    (on_crash restart)
    (uuid 0004fb00-0006-0000-236e-45007b980aa1)
    (bootloader_args -q)
    (name 0004fb0000060000236e45007b980aa1)
    (on_reboot restart)
    (maxmem 2048)
    (memory 2048)
    (shadow_memory 0)
    (features '')
    (on_xend_start ignore)
    (on_xend_stop ignore)
    (start_time 1467059760.94)
    (cpu_time 266.840330081)
    (online_vcpus 2)
    (image
        (linux
            (kernel '')
            (expose_host_uuid 0)
            (superpages 0)
            (videoram 4)
            (pci ())
            (nomigrate 0)
            (tsc_mode 0)
            (device_model /usr/lib/xen/bin/qemu-dm)
            (notes
                (HV_START_LOW 4118806528)
                (FEATURES '!writable_page_tables|pae_pgdir_above_4gb')
                (VIRT_BASE 3221225472)
                (GUEST_VERSION 2.6)
                (PADDR_OFFSET 0)
                (GUEST_OS linux)
                (HYPERCALL_PAGE 3225427968)
                (LOADER generic)
                (SUSPEND_CANCEL 1)
                (PAE_MODE yes)
                (ENTRY 3232718848)
                (XEN_VERSION xen-3.0)
            )
        )
    )
    (status 2)
    (state -b----)
    (store_mfn 2547788)
    (console_mfn 2547787)
    (device
        (vif
            (bridge 10e69b4de3)
            (mac 00:21:f6:00:08:b8)
            (script /etc/xen/scripts/vif-bridge)
            (uuid 834beea5-71e6-2b04-7fe1-6d8c1f5d1930)
            (backend 0)
        )
    )
    (device (vkbd (backend 0)))
    (device
        (console
            (protocol vt100)
            (location 2)
            (uuid 476bd2b4-097b-2d1f-62f1-45dda9a35272)
        )
    )
    (device
        (vbd
            (protocol x86_32-abi)
            (uuid 460f1c61-09c8-18cc-156a-9c54e324c6b9)
            (bootable 1)
            (dev xvda:disk)
            (uname
                file:/OVS/Repositories/0004fb0000030000a5c9b5cf920f93e3/VirtualDisks/0004fb0000120000e77ab5d916c6c3c2.img
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
            (uuid fbd8f384-13a4-d080-2b53-53adf22d8c5f)
            (vnclisten 127.0.0.1)
            (keymap en-us)
            (location 127.0.0.1:5900)
            (xauthority /root/.Xauthority)
        )
    )
)
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
    (cpu_time 5015.16446156)
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
(domain
    (domid 0)
    (cpu_weight 65535)
    (cpu_cap 0)
    (pool_name Pool-0)
    (bootloader '')
    (vcpus 2)
    (cpus ((0 1 2 3 4 5 6 7) (0 1 2 3 4 5 6 7)))
    (on_poweroff destroy)
    (on_crash restart)
    (uuid 00000000-0000-0000-0000-000000000000)
    (bootloader_args '')
    (name Domain-0)
    (on_reboot restart)
    (maxmem 1104)
    (memory 1098)
    (shadow_memory 0)
    (features '')
    (on_xend_start ignore)
    (on_xend_stop ignore)
    (cpu_time 105443.858723)
    (online_vcpus 2)
    (image
        (linux
            (kernel '')
            (expose_host_uuid 0)
            (superpages 0)
            (nomigrate 0)
            (tsc_mode 0)
        )
    )
    (status 2)
    (state r-----)
)
"""

def get_domains_info():
    """
    Retrieve from OVS server Xen domains information
    and serialize it to internal objects representation.
    OVS server returns the data encoded in 'symbolic expression'
    (Lisp programming language notation) format.
    """
    domains = []
    info = s
    info_sxp = sxp.all_from_string(info)
    # print info_sxp
    result = []
    for dom_info in info_sxp:
        dom = DomainInfo(dom_info)
        domains.append(dom)
        # print "<<<<<<<<<<<<<<<"
        # print dom.to_json()
        # print ">>>>>>>>>>>>>>>"
    return result

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

if __name__ == "__main__":
    l = get_domains_info()
    #print type(l)
    #for e in l:
    #    print "===> %s" % type(e)
    
    
    
    
    
    
    
    
