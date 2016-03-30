#! /usr/bin/python

import eventlet
from eventlet.green import urllib2

urls = ["http://www.sian.com","http://www.ltaaa.com",
	"http://www.baidu.com"]

def fetch(url):
	return lirlib2.urlopen(url).read()

pool = eventlet.GreenPool()
for body in pool.imap(fetch,urls):
	print body
