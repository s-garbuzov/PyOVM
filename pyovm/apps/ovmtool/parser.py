#!/usr/bin/env python

import sys
import os

import yaml

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from components.linux import Linux

__all__ = []
__version__ = 0.1
__date__ = '2016-07-14'
__updated__ = '2016-07-14'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class OVMCfg():
    """ Attributes necessary for communication with OVS server(s) """

    def __init__(self, host, port, name, pswd):
        self.host = host
        self.port = port
        self.admin_name = name
        self.admin_pswd = pswd

    def to_string(self):
        return "%s:%s" % (self.host, self.port)

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "%s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2016 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-i", "--include", dest="include", help="only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]", metavar="RE" )
        parser.add_argument("-e", "--exclude", dest="exclude", help="exclude paths matching this regex pattern. [default: %(default)s]", metavar="RE" )
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')

        # Process arguments
        args = parser.parse_args()

        paths = args.paths
        verbose = args.verbose
        recurse = args.recurse
        inpat = args.include
        expat = args.exclude

        if verbose > 0:
            print("Verbose mode on")
            if recurse:
                print("Recursive mode on")
            else:
                print("Recursive mode off")

        if inpat and expat and inpat == expat:
            raise CLIError("include and exclude pattern are equal! Nothing will be processed.")

        for inpath in paths:
            ### do something with inpath ###
            print(inpath)
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

class MyParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(MyParser, self).__init__(*args, **kwargs)
        #ArgumentParser.__init__(self, *args, **kwargs)

    def error(self, message): 
        s = "\nError: %s\n\n%s" % (message, self.format_usage())
        raise CLIError(s)

class CLIExecuter(object):
    """ CLI commands parser and executer """
    def __init__(self, *cmd_opts):
        self.prog = 'ovm'

        """
        parser = MyParser(
            prog=self.prog,
            description=("Command line tool for interaction with "
                         "OpenFlow Controller"),
            usage=("%(prog)s [-h] [-C <path>] <command> [<args>]\n"
                   "('%(prog)s -h' for details)\n"
                   "\nAvailable commands are:\n"
                   "\n   show-ovs      Show OVS server information"
                   "\n   show-net      Show network information"
                   "\n   show-eth      Show ethernet interfaces"
                   "\n   show-ib       Show infiniband interfaces"
                   "\n   show-bonding  Show bonding information"
                   "\n   show-bridge   Show bridging information"
                   "\n   show-cluster  Show cluster information"
                   "\n"))
         """
        usage_str = ("%(prog)s [-h] [-C <path>] <command> [<args>]\n"
                     "('%(prog)s -h' for details)\n"
                   "\nAvailable commands are:\n")
        #cmds_str = "   \n".join(show_cmds.keys())
        cmds_str = ""
        for k, v in show_cmds.items():
            cmds_str += "   %-15s - %s\n" % (k, v[1])
        #cmds_str = ["   %s\n" % k for k in show_cmds.keys()]
        #print "A=   %s" % cmds_str

        usage_str += "%s" % cmds_str
        parser = MyParser(
            prog=self.prog,
            description=("Command line tool for interaction with "
                         "OpenFlow Controller"),
            usage=usage_str)

        parser.add_argument('-C', metavar="<path>",
                            dest='cfg_file',
                            help="path to the OVM configuration file "
                                 "(default is './ovm.yml')",
                            default="./ovm.yml")
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
    luns = linux.discover_physical_luns()
    print luns.to_json()

def show_mounted_fs(dst, *args):
    linux = Linux(dst)
    nfs = linux.discover_mounted_file_systems()
    print nfs.to_json()

def show_repos(dst, *args):
    linux = Linux(dst)
    repos = linux.package_get_repositories()
    print repos.to_json()

def show_pkgs(dst, *args):
    linux = Linux(dst)
    pkgs = linux.package_list()
    print pkgs.to_json()

def show_disk_space(dst, *args):
    linux = Linux(dst)
    dsk = linux.get_system_disk_space()
    print dsk.to_json()

def show_boot_time(dst, *args):
    linux = Linux(dst)
    bt = linux.get_last_boot_time()
    print bt.to_json()

def show_ntp(dst, *args):
    linux = Linux(dst)
    ntp = linux.get_ntp()
    print ntp.to_json()

def show_time(dst, *args):
    linux = Linux(dst)
    t = linux.get_datetime()
    print t.to_json()

def show_timezone(dst, *args):
    linux = Linux(dst)
    tz = linux.get_timezone()
    print tz.to_json()

def show_log(dst, *args):
    linux = Linux(dst)
    log = linux.get_log()
    print log.to_json()


def show_network(dst, *args):
    print("show_network")

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

show_cmds = {
    'show-ovs': [show_ovs, 'Show OVS server generic info'],
    'show-hardware': [show_hardware, 'Show hardware info'],
    'show-luns': [show_physical_luns, 'Show LUNs info'],
    'show-nfsmnt': [show_mounted_fs, 'Show mounted file systems'],
    'show-yum': [show_repos, 'Show YUM repositories'],
    'show-pkgs': [show_pkgs, 'Show installed packages'],
    'show-disk-space': [show_disk_space, 'Show system disk space'],
    'show-boot-time': [show_boot_time, 'Show last boot time'],
    'show-ntp': [show_ntp, 'Show NTP info'],
    'show-time': [show_time, 'Show date and time'],
    'show-tz': [show_timezone, 'Show timezone'],
    'show-log': [show_log, 'Display log content']
}
"""
'show-net': show_network,
'show-eth': show_eth,
'show-ib': show_infiniband,
'show-bond': show_bonding,
'show-bridge': show_bridge,
'show-cluster': show_cluster,
"""

if __name__ == "__main__":
    #print type(sys.argv)
    try:
        CLIExecuter(sys.argv)
    #except (Exception, SystemExit) as e:
    except (CLIError) as e:
        print "%s" % e
        #print "AAA"
        #sys.stderr.write("ovmtool"+ ": " + repr(e) + "\n")
    #sys.exit(CLIParser())
    except (Exception) as e:
        print "%s" % repr(e)

    
    '''
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'ovs.parser_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
    '''