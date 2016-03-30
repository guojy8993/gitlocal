#! /usr/bin/python

import os
def get_localhost():
	return os.environ['HOSTNAME']

if __name__ == "__main__":
	print get_localhost()
