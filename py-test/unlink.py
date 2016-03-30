#! /usr/bin/python

import os

path = "/tmp/tmp/123.txt"

dir_name = os.path.dirname(path)
print dir_name

if os.path.isdir(dir_name):
	os.unlink(path)

