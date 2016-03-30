#! /usr/bin/python

import os
import subprocess

p1 = subprocess.Popen(["ls","/root"],stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep","py"],stdin=p1.stdout,stdout=subprocess.PIPE)
p1.stdout.close()
print p2.communicate()[0]

#retv = subprocess.check_output(["ip","route","|","grep","10"])
#print retv
