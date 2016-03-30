#! /usr/bin/python

import threading

def job(i):
	print "Thread %d starts working"%i
	print i
	print "Thread %d's job done"%i

if __name__ == "__main__":
	workers = []
        for i in xrange(10):
		thread = threading.Thread(target=job,args=(i,))
		thread.start()
		workers.append(thread)
	
	for worker in workers:
		worker.join()
	
	print "All Job done."
