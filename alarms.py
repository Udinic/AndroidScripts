#!/usr/bin/env python

"""
    Alarms.py

    Prints all the alarms scheduled for one package name, or the entire system

    Usage: python alarms.py [<package name>]

"""

__author__ = 'Udi Cohen <udinic@gmail.com>'
__license__ = "Apache 2.0"
__copyright__ = 'Copyright 2012 Udi Cohen'

import subprocess
import re
from subprocess import *
import sys, pprint

print '              **********************************'
print '              *      Android Alarms Dumper     *'
print '              *                                *'
print '              *       Written by Udi Cohen     *'
print '              *       http://www.udinic.com    *'
print '              **********************************'
print
print

p=subprocess.Popen([r'adb', 'shell', 'dumpsys alarm'],
                       stdout=PIPE, stderr=PIPE,
                       shell= True,
                       cwd='C:\\')
out, err = p.communicate()
p.wait()

pp = pprint.PrettyPrinter(indent=4)
        
lines= out.split('\n')
alerts = [["RTC TYPE", "When", "Repeat", "pkg", "Type"]]

for i in xrange(len(lines)):
    if lines[i].replace(" ","")[:3]=="RTC":

        # Extract the information we
        rtc_type = lines[i].strip().split()[0]
        when=re.findall('when=([0-9a-z+]*)',lines[i+1])[0]
        repeat=re.findall('repeatInterval=([0-9a-z+])*',lines[i+1])[0]
        intentType=list(re.findall("PendingIntentRecord{(\w+) ([\w\.]+) (\w+)", lines[i+2])[0])

        # If the user has passed a package name as an argument
        # we'll filter all other packages' alarms
        if len(sys.argv) > 1:
            if intentType[1] == sys.argv[1]:
                alerts.append([rtc_type, when, repeat, intentType[1], intentType[2]])
        else:
            alerts.append([rtc_type, when, repeat, intentType[1], intentType[2]])

out_lines = [""] * len(alerts)

# Format the data nicely to columns
for column in xrange(len(alerts[0])):

    for alert_index in xrange(len(alerts)):
        out_lines[alert_index] += str(alerts[alert_index][column])

    line_size = max(map(len, out_lines)) + 5

    for alert_index in xrange(len(alerts)):
        out_lines[alert_index] += " " * (line_size - len(out_lines[alert_index]))

for l in out_lines:
    print l

print	
raw_input("Press ENTER to exit")
