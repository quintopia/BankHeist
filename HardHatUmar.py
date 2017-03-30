import sys

game = int(sys.argv[1])
round = int(sys.argv[2])
hired = int(sys.argv[12])

if round==1:
    if game < 800 and hired:
        print 1
    else:
        print 0
else:
    print "change jobs"