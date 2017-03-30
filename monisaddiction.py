import sys
import random


round = int(sys.argv[2])
myrank = int(sys.argv[13])
mybet = int(sys.argv[10])

if round == 1:
    if random.random()<0.1:
        print 1
    else:
        print 69
else:
    if myrank>1:
        print "all in"
    else:
        if mybet==1:
            print "back out"
        else:
            print "!guncheck"
        