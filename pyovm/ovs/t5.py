'''
Created on Jul 14, 2016

@author: sergei
'''
import os
import subprocess

path="/home/sergei/work/myprojects/PyOVM/pyovm/apps/ovmtool/manpages/m1"
cmd = ['man', path, "|less"]
p = subprocess.Popen(cmd, stdout=None,
                     stderr=subprocess.PIPE,
                     stdin=subprocess.PIPE,
                     shell=False)
out, err = p.communicate()
print(out)
