#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import signal
import Queue
from time import sleep

QCOUNT = Queue.Queue()  # initializing Queue

def onsigchld(signum,frame):
	print "SIGCHLD received !"
	sleep(2)
	QCOUNT.put(1)

def exithandler(signum,frame):
	print "Exit"
	raise SystemExit("SIGINT received !")

signal.signal(signal.SIGUSR1,onsigchld)    # bind signal with handler
signal.signal(signal.SIGINT,exithandler)


while 1:
	print "Main: %d " % os.getpid()
	print "Elements count in Queue: %d " % QCOUNT.qsize()
	sleep(2)
























