#!/usr/bin/env python

"""
    Activities.py

    Prints the activities stack of a specific package name or the whole system.

    Usage: python activities.py [<package name>]

"""

__author__ = 'Udi Cohen <udinic@gmail.com>'
__license__ = "Apache 2.0"
__copyright__ = 'Copyright 2012 Udi Cohen'

import subprocess
import re
from subprocess import *
import sys
import os

def printStack(app_name):
    lines= out.split('\n')
    curr_pkg = ""
    compiled1 = re.compile("Run .*?HistoryRecord{\S+\s(" + app_name + ")/\\.(.*?)\\}")
    compiled2 = re.compile("Run .*?ActivityRecord{\S+\s(" + app_name + ")/\\.(.*?)\\}")
    print "======== Activity Stack =========="
    for i in xrange(len(lines)):
        activity=re.findall(compiled1,lines[i])
        if not activity:
            activity=re.findall(compiled2,lines[i])
            
        if (activity):
            if curr_pkg != activity[0][0]:
                curr_pkg = activity[0][0]
                print curr_pkg 
            print "\t" + activity[0][1]
    print "=================================="
    
print '              **********************************'
print '              *      Activity stack viewer     *'
print '              *                                *'
print '              *       Written by Udi Cohen     *'
print '              *       http://www.udinic.com    *'
print '              **********************************'
print
print

p=subprocess.Popen([r'adb', 'shell', 'dumpsys activity activities'],
                       stdout=PIPE, stderr=PIPE,
                       shell= True,
                       cwd=os.getenv("HOME"))
out, err = p.communicate()
p.wait()

app = ".*?"
if len(sys.argv) > 1:
    app = sys.argv[1]

printStack(app)

print
raw_input("\nPress ENTER to exit")                                
