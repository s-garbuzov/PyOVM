sample = """
[2016-07-18 17:34:40 3173] INFO (xmlrpc:407) Oracle VM Server version: {'release': '3.4.1', 'date': '201603010859', 'build': '1350'}, hostname: ovs235, ip: 10.137.124.235
[2016-07-18 17:34:40 3173] INFO (xmlrpc:422) Oracle VM Agent XMLRPC Server started.
[2016-07-18 17:34:44 3165] DEBUG (monitor:39) Cluster state changed from [Unknown] to [Offline]
[2016-07-18 17:34:51 3301] ERROR (xmlrpc:133) Unauthorized access attempt from ('10.149.238.168', 44252)!
Traceback (most recent call last):
  File "/usr/lib64/python2.6/site-packages/agent/daemon/xmlrpc.py", line 128, in do_POST
    auth(username, password)
  File "/usr/lib64/python2.6/site-packages/agent/daemon/xmlrpc.py", line 93, in auth
    raise Exception('Authorization Failed')
Exception: Authorization Failed
[2016-07-18 17:34:51 3301] INFO (xmlrpc:254) code 403, message Unauthorized access attempt from ('10.149.238.168', 44252)!
[2016-07-18 17:35:11 3393] ERROR (xmlrpc:133) Unauthorized access attempt from ('10.149.238.168', 44271)!
Traceback (most recent call last):
  File "/usr/lib64/python2.6/site-packages/agent/daemon/xmlrpc.py", line 128, in do_POST
    auth(username, password)
  File "/usr/lib64/python2.6/site-packages/agent/daemon/xmlrpc.py", line 93, in auth
    raise Exception('Authorization Failed')
Exception: Authorization Failed
[2016-07-18 17:35:11 3393] INFO (xmlrpc:254) code 403, message Unauthorized access attempt from ('10.149.238.168', 44271)!
"""

#r=[]
info_pattern = ' INFO '
dbg_pattern = ' DEBUG '
warn_pattern = ' WARNING '
err_pattern = ' ERROR '

msgs = {info_pattern: [],
        dbg_pattern: [],
        warn_pattern: [],
        err_pattern: []
}

info = []
dbg = []
warn = []
err = []
msg_type = None

slist = sample.split("\n")
t = []
for s in slist:
    if s.startswith('['):
        if msg_type and t:
            msgs[msg_type].append("\n".join(t))
            t = []

        if s.find(info_pattern) != -1:
            msg_type = info_pattern
        elif s.find(dbg_pattern) != -1:
            msg_type = dbg_pattern
        elif s.find(warn_pattern) != -1:
            msg_type = warn_pattern
        elif s.find(err_pattern) != -1:
            msg_type = err_pattern
        else:
            assert(False)
            continue
        msgs[msg_type].append("%s\n" % s)
    else:
        t.append(s)

print("<<<<<").strip()
print("Errors:")
#msg = msgs[err_pattern]
for msg in msgs[err_pattern]:
    if msg.startswith('['):
        print("\n").strip()
    print("%s" % msg).strip()
print(">>>>>")





"""
slist = sample.split("\n")
t = []
for s in slist:
    if s.startswith('['):
        if msg_type and t:
            records[msg_type].append("\n".join(t))
            t = []

        if s.find(info_pattern) != -1:
            msg_type = info_pattern
        elif s.find(dbg_pattern) != -1:
            msg_type = dbg_pattern
        elif s.find(warn_pattern) != -1:
            msg_type = warn_pattern
        elif s.find(err_pattern) != -1:
            msg_type = err_pattern
        else:
            assert(False)
            continue
        #print "* %s (%s)" % (s, msg_type)
        records[msg_type].append("%s\n" % s)
        r.append("%s\n"%s)
        #r.append(s)
    else:
        #print("2) ***%s" % s)
        t.append(s)
"""




"""
r=[]
err = []
slist = sample.split("\n")
t = []
for s in slist:
    if s.startswith('['):
        if t:
            r.append("\n".join(t))
            t = []
        print("1) ***%s" % s)
        r.append("%s\n"%s)
        #r.append(s)
    else:
        print("2) ***%s" % s)
        t.append(s)

print("<<<<<").strip()
#print r
for i in r:
    print("%s" % i).strip()
print(">>>>>")
"""






"""
import re
sample = sample.strip("\n")
#sample = sample
#print sample
#match = re.search(r'[.*]', s, re.DOTALL)
#r = re.findall(r'[.*]', sample, re.MULTILINE)
#r = re.findall(r'2016', sample)
r = re.split(r'\[.*\]', sample, re.MULTILINE)
#print type(r)
for i in r:
    print "***%s" % i
"""







