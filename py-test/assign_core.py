#! /usr/bin/python

require = {
  "1":1,
  "2":4,
  "3":12,
  "4":8,
  "5":4
}

all = 64 #16

def assign(require,all):
        i=0
	for k,v in require.iteritems():
                cores = [p%all for p in xrange(i,i+v)]
                i=i+v
                require.update({k:cores})
	#print require			


if __name__ == "__main__":
	assign(require,all)
        print require





























