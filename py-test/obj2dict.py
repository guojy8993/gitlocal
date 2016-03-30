#! /usr/bin/python

class O(object):
	def __init__(self):
		self.name = "123"
		self.age = 123

print O().__dict__
print O().__class__
