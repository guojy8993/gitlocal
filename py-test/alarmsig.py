#! /usr/bin/env python
# -*- coding;utf-8 -*-

import signal
import time

def onReceiveAlarm(signum,frame):
	print "Alarm : %s" % time.ctime()

signal.signal(signal.SIGALRM,onReceiveAlarm)
signal.alarm(2)

print "Before: %s" % time.ctime()
time.sleep(100)
print "Post: %s" % time.ctime()



































