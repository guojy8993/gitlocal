#! /usr/bin/python

matchable = {}
matchable[0x123] = 123
print matchable[0x123]
print 0x123 in matchable 
matchable[123] = 245
print matchable[123]

ff = dict()
ff.update({12:34})
print ff[12]
