#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import signal
from time import sleep

def handler(signum,frame):
	print signum
	print type(frame)
	print "Signal Received !"

signal.signal(signal.SIGTERM,handler)

def handler2(signal,frame):
	print "Signal 2"

signal.signal(signal.SIGUSR1,handler2)

while 1:
	print os.getpid()
	sleep(100)


































