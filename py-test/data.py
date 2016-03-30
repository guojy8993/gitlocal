#! /usr/bin/python
# -*- coding:utf-8 -*-
import time
import threading
import os
import sys


a = 1
print a
a = 1.23
print a

a = "no"
print a

b = "guojy"
print a,b

c = {}
c["name"] = "lee"
c["age"] = 24
print c
c.update({"age":34})
print c

d = []
d.append("we")
d.append(123)
d.append(456)
d.append(456)
print d

f = d[:]
print f

f = d[2:]
print f

f = d[:3]
print f

f = d[:-2]
print f

g = [i for i in d if str(i).isdigit() ]
print g

h = set(d)
print h


i = " HelloWorld!"
print i[:-1]

j = "#mysql_db=default"

if j.startswith("#"):
	j = j[1:]
print j	

l = i.split("llo")
print l


i = "___".join(l) 
print i

"""
m = i.index("___")
print m
"""

if i is None:
	print "i is None"
elif len(i) > 0:
	print "length of i: %d" % (len(i))
else:
	pass


""" range """
"""
for i in range(10):
	print i
"""

n =   "no" if  len(i) > 0 else "yes"
print n


"""
def task(task_no):
	print "task %d is running !"%task_no
	time.sleep(3)	

threads = []
for  task_no in range(10):
	th = threading.Thread(target=task,args=(task_no,))
	th.start()
	threads.append(th)

for th in threads:
	th.join()
"""
print "====="

type = None
if os.path.exists("/home/test"):
	type = "a"
else:
	type = "w"
f = open("/home/test",type)
f.write("***")
f.close()

f = open("/home/test","r")
content = f.read()
f.close()

print content

class People(object):
	def __init__(self,name,age):
		self.name = name
		self.age = age
	def show(self):
		print "i am %s , and i'am %d years old"%(self.name,self.age)


GuoJy = People("guojy",26)
GuoJy.show()

"""
args = sys.argv[1:]
print args



dst = open("/home/%s" % args[0],"a")
dst.write("&&&&")
dst.close()
"""


prompt = raw_input("请输入名字:")
if prompt is not None and len(prompt) > 0 :
	print "尊敬的%s您好!"%prompt
else:
	print "请输入名字!"




