#!/usr/bin/env python

import xmltodict
import xml.etree.ElementTree as xml
from pyovm.utils.xmlrpclib import ServerProxy, Error, dumps

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)

class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})

def my_postprocessor(path, key, value):
    # print("A1 path=%s, key=%s, value=%s" % (path, key, value))
    return (key.lower(), value)



if __name__ == "__main__":

    # simple test program (from the XML-RPC specification)

    # server = ServerProxy("http://localhost:8000") # local server
    # server = ServerProxy("http://time.xmlrpc.com/RPC2")
    uri = "https://%s:%s@%s" % ("oracle", "oracle", "ovs235:8899/RPC2")
    #uri = "https://%s:%s@%s" % ("oracle", "oracle", "ovs240:8899/RPC2")
    #uri = "https://%s:%s@%s" % ("oracle", "oracle", "ovs233:8899/RPC2")
    #uri = "https://%s:%s@%s" % ("oracle", "oracle", "ovs235:8899/RPC2")
    # "http://user:pass@host:port/path"
    
    server = ServerProxy(uri, verbose=0)

    print("***GSF: server=%s, uri=%s" % (server, uri))

    try:
        # print server.currentTime.getCurrentTime()
        import json
        # r = server.get_api_version()

        #
        # Repositories
        #
        #XML? r = server.discover_repositories("0004fb0000030000a5c9b5cf920f93e3")
        #XML? r = server.discover_repositories("0004fb00000300002160f6433014d23a")
        # r = server.get_repository_meta_data("0004fb00000300002160f6433014d23a")
        #XML?
        r = server.discover_repository_db()

        #
        # Server Poll
        #
        #XML? r = server.discover_server_pool()

        #
        # Plugin Manager (plugins under /opt/storage-connect)
        #
        #XML? r = server.discover_storage_plugins()
        
        #
        # o2cb
        #
        #XML? r = server.discover_cluster()
        # r = server.is_cluster_online()

        #
        # Linux
        #
        #r = server.get_last_boot_time()
        #r = server.get_system_disk_space()
        #XML? r = server.discover_physical_luns('',)
        #r = server.package_list("installed")
        #r = server.package_list("updates")
        
        #l = ['messages', 'dmesg', 'xend', 'ovs-agent']
        #r = server.get_log(l)
        #for k, v in r.items():
        #    print v
        
        #XML? r = server.discover_hardware()
        
        # r = server.get_datetime()
        #XML? 
        #r = server.discover_server()
        #XML? r = server.discover_mounted_file_systems("all")
        #XML? r = server.discover_mounted_file_systems("nfs4")
        #r = server.discover_mounted_file_systems("ocfs2")
        #r = server.discover_mounted_file_systems("rootfs")
        
        #
        # Xen
        #
        # r = server.list_vms()
        #r = server.list_vm("0004fb00000300002160f6433014d23a", "0004fb00000600007c522c7d71072a52")
        #r = server.list_vm_core("0004fb00000300002160f6433014d23a", "0004fb00000600007c522c7d71072a52")
        #r = server.get_vm_config("0004fb00000300002160f6433014d23a", "0004fb00000600007c522c7d71072a52")

        #
        # Network
        #
        #XML? 
        #r = server.discover_network()
        
        
        assert(isinstance(r, tuple))
        if(isinstance(r[0], basestring)):
            s='<?xml version'
            if s in r[0]:
                print "YES!!!"
                #print r[0]
                
                d = xmltodict.parse(xml_input=r[0],
                                    xml_attribs=True,
                                    process_namespaces=True,
                                    postprocessor=my_postprocessor)
                """
                d = xmltodict.parse(xml_input=r[0],
                                    xml_attribs=True,
                                    process_namespaces=True)
                """
                print json.dumps(d, indent=4)
        else:
            print "No!!!"
            print json.dumps(r[0], indent=4)
        #print json.dumps(doc, indent=4)
        # print r[0]
        exit(0)
        
        
        #print r
        if(isinstance(r, tuple)):
            cnt = 0
            for e in r:
                root = xml.fromstring(e)
                print "root.tag=%s" % root.tag
                xmldict = XmlDictConfig(root)
                print "<<<"
                #print xmldict
                print json.dumps(xmldict, indent=4)
                print ">>>"
                """
                print "root.attrib=%s" % root.attrib
                for child in root.iter():
                    # print child.attrib
                    print child.tag
                """
                
                """
                cnt += 1
                #print("+=+ %s (type=%s)" % (e, type(e)))
                root = xml.fromstring(e)
                for child in root:
                    print child.tag, child.attrib
                
                #print type(root)
                #print "dir=%s" % dir(root)
                #print "vars=%s" % vars(root)
                #print "%s" % root.tag
                #print("%s" % "".join(root.iterchildren()))
                #r1 = xml.parse(root)
                #print("%s" % "".join(root.itertext()))
                #print("%s" % r1)
                """
        #print r

        #print json.dumps(r, indent=4)
        #return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
        #                  indent=4)
        # print server.list_vms()
    except Error, v:
        print "ERROR", v
