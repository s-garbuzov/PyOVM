#!/usr/bin/env python

import sys
# import os
# import ordereddict
import yaml

from collections import OrderedDict
from argparse import ArgumentParser
# from argparse import RawDescriptionHelpFormatter

from components.linux import Linux

__all__ = []
__version__ = 0.1
__date__ = '2016-07-14'
__updated__ = '2016-07-14'

DEBUG = 1
TESTRUN = 0
PROFILE = 0


class OVMCfg():
    """
    Placeholder for attributes that are necessary for
    communication with OVS server(s)
    """

    def __init__(self, host, port, name, pswd):
        self.host = host
        self.port = port
        self.admin_name = name
        self.admin_pswd = pswd

    def to_string(self):
        return "%s:%s" % (self.host, self.port)


class CLIError(Exception):
    """Generic exception to raise and log different fatal errors."""
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "%s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


class CLIParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(CLIParser, self).__init__(*args, **kwargs)
        # ArgumentParser.__init__(self, *args, **kwargs)

    def error(self, message):
        s = "\nError: %s\n\n%s" % (message, self.format_usage())
        raise CLIError(s)


class CLIExecuter(object):
    """ CLI commands parser and executer """
    def __init__(self, *cmd_opts):
        self.prog = 'rpc-show'
        usage_str = ("%(prog)s [-h] [-C <path>] <command> [<args>]\n"
                     "('%(prog)s -h' for details)\n"
                     "\nAvailable commands are:\n")
        cmds_str = ""
        for k, v in show_cmds.items():
            cmds_str += "   %-15s - %s\n" % (k, v[1])
        usage_str += "%s" % cmds_str

        parser = CLIParser(
            prog=self.prog,
            description=("Command line tool for interaction with "
                         "OpenFlow Controller"),
            usage=usage_str
            )

        parser.add_argument('-C', metavar="<path>",
                            dest='cfg_file',
                            help="path to the OVM configuration file "
                                 "(default is './ovscfg.yml')",
                            default="./ovscfg.yml")
        parser.add_argument('command', help='command to be executed')

        args, remaining_args = parser.parse_known_args()

        # Get attributes from configuration file
        try:
            self.cfg = self.get_cfg(args.cfg_file)
        except (IOError):
            s = "\nError: %s\n" % ("Cannot find configuration file")
            raise CLIError(s)
        except (KeyError):
            s = "\nError: %s\n" % ("Malformed data in configuration file")
            raise CLIError(s)

        # Execute the command
        try:
            show_cmds[args.command][0](self.cfg, remaining_args)
        except KeyError:
            s = "\nError: %s '%s'\n\n%s" % ("unknown command",
                                            args.command,
                                            parser.format_usage())
            raise CLIError(s)

    def get_cfg(self, path):
        with open(path, 'r') as f:
            obj = yaml.load(f)
        d = {}
        for k, v in obj.iteritems():
            d[k] = v

        host = d['host']
        port = d['port']
        name = d['name']
        pswd = d['pswd']
        cfg = OVMCfg(host, port, name, pswd)
        return cfg


def show_ovs(dst, *args):
    linux = Linux(dst)
    srv = linux.discover_server()
    print srv.to_json()


def show_hardware(dst, *args):
    linux = Linux(dst)
    hw = linux.discover_hardware()
    print hw.to_json()


def show_physical_luns(dst, *args):
    linux = Linux(dst)
    linux.discover_physical_luns()
    if linux.scsi_disks:
        for e in linux.scsi_disks:
            print e.to_json()
    if linux.scsi_targets:
        for e in linux.scsi_targets:
            print e.to_json()


def show_mounted_fs(dst, *args):
    linux = Linux(dst)
    nfs = linux.discover_mounted_file_systems()
    for item in nfs:
        print("%s" % item.to_json())


def show_repos(dst, *args):
    linux = Linux(dst)
    repos = linux.package_get_repositories()
    print repos.to_json()


def show_pkgs(dst, *args):
    linux = Linux(dst)
    linux.package_list('installed')
    if linux.pkgs_installed:
        for pkg in linux.pkgs_installed:
            print pkg.to_json()
    linux.package_list('updates')
    if linux.pkgs_updates:
        for pkg in linux.pkgs_installed:
            print pkg.to_json()


def show_disk_space(dst, *args):
    linux = Linux(dst)
    ds = linux.get_system_disk_space()
    print ds.to_json()


def show_boot_time(dst, *args):
    linux = Linux(dst)
    bt = linux.get_last_boot_time()
    print("\n").strip()
    print("  Current Time  : %s" % bt.current_time())
    print("  Last Boot Time: %s" % bt.boot_time())
    print("\n").strip()


def show_ntp(dst, *args):
    linux = Linux(dst)
    ntp = linux.get_ntp()
    print ntp.to_json()


def show_datetime(dst, *args):
    linux = Linux(dst)
    t = linux.get_datetime()
    print("\n").strip()
    print("   %s" % (t.to_str()))
    print("\n").strip()
    # print t.to_json()


def show_timezone(dst, *args):
    linux = Linux(dst)
    tz = linux.get_timezone()
    print("\n").strip()
    print("   %s" % (tz.to_str()))
    print("\n").strip()
    # print tz.to_json()


def show_repository_db(dst, *args):
    print("show_repository_db")
    linux = Linux(dst)
    repos = linux.discover_repository_db()
    for repo in repos:
        print("%s" % repo.to_json())


def show_log(dst, *args):
    linux = Linux(dst)
    # l = ["messages", "dmesg"]
    # logfile = 'messages'
    # logfile = 'dmesg'
    # logfile = 'xend'
    logfile = 'ovs-agent'
    log = linux.get_log(logfile)
    try:
        # print("%s" % log.to_str())
        # print "%s" % log.errors()
        print "%s" % log.warnings()
        # print "%s" % log.info()
        # print "%s" % log.debug()
        pass
    except (KeyboardInterrupt, SystemExit):
        print "!!!!!!!!\n\n"
        raise "!!!!!!!!\n\n"


def show_network(dst, *args):
    # print("show_network")
    linux = Linux(dst)
    nw = linux.discover_network()
    print nw.to_json()
    # print srv.to_json()


def show_eth(dst, *args):
    print("show_eth")


def show_infiniband(dst, *args):
    print("show_infiniband")


def show_bonding(dst, *args):
    print("show_bonding")


def show_bridge(dst, *args):
    print("show_bridge")


def show_cluster(dst, *args):
    print("show_cluster")


show_cmds = OrderedDict((
    ('server', [show_ovs, 'Show OVS server generic info']),
    ('hardware', [show_hardware, 'Show hardware info']),
    ('network', [show_network, 'Show network info']),
    ('phy-luns', [show_physical_luns, 'Show physical LUNs info']),
    ('nfsmnt', [show_mounted_fs, 'Show mounted file systems']),
    ('yum', [show_repos, 'Show YUM repositories']),
    ('pkgs', [show_pkgs, 'Show installed packages']),
    ('disk-space', [show_disk_space, 'Show system disk space']),
    ('boot-time', [show_boot_time, 'Show last boot time']),
    ('ntp', [show_ntp, 'Show NTP info']),
    ('datetime', [show_datetime, 'Show date and time']),
    ('timezone', [show_timezone, 'Show timezone']),
    ('repo-db', [show_repository_db, 'Show repositories']),
    ('log', [show_log, 'Display log content']),
))

"""
'show-net': show_network,
'show-eth': show_eth,
'show-ib': show_infiniband,
'show-bond': show_bonding,
'show-bridge': show_bridge,
'show-cluster': show_cluster,
"""

if __name__ == "__main__":
    try:
        CLIExecuter(sys.argv)
    except (CLIError) as e:
        print "%s" % e
        exit(1)
    except KeyboardInterrupt:
        # handle keyboard interrupt
        exit(0)
    except (Exception) as e:
        print "%s" % repr(e)
        exit(1)
