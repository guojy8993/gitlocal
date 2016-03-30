#! /usr/bin/python

import os
import time
import threading

conf_path = "/root/test"

def get_interval():
	if os.path.exists(conf_path):
		open_type = "r"
	else:
		open_type = "a"
	f = open(conf_path,open_type)
	content = f.read()
	f.close()
	content = content.strip()
	if len(content) == 0:
		return 3
	else:
		return int(content)

interval = 2

def update_conf():
	while True:
		global interval 
		interval = get_interval()
		time.sleep(1)

th = threading.Thread(target=update_conf)
th.start()

time.sleep(1)

while True:
	print "Please wake me up in %d seconds "%interval
	time.sleep(interval)
	


