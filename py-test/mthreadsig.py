#! /usr/bin/env python
# -*- coding:utf-8 -*-

import signal
import threading
import os
import time

def signal_handler(signum,frame):
	print "Signal %d Received in Thread %s " % (signum,threading.currentThread().name)

signal.signal(signal.SIGUSR1,signal_handler)

def wait_for_signal():
	print "Waiting for signal in %s" % threading.currentThread().name
	signal.pause()
	print "Done waiting."

receiver = threading.Thread(target=wait_for_signal,name='receiver')
receiver.start()
time.sleep(0.1)

def send_signal():
	print "Sending signal in %s " % threading.currentThread().name
	os.kill(os.getpid(),signal.SIGUSR1)

sender = threading.Thread(target=send_signal,name='sender')
sender.start()
sender.join()

print "Waiting for %s " % receiver.name
signal.alarm(2)
receiver.join()


























"""
signal.pause() -> https://docs.python.org/2/library/signal.html#signal.pause
"""






































