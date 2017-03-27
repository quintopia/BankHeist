import sys
import random
import ast

game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,p,b,myyattas,mybet,mypayment,bank0,bank1,bank2,bank3,bank4,myrank,mu_yattas,sigma_yattas,max_yattas = map(ast.literal_eval,sys.argv[1:])

sys.stderr.write(str(myrank))
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
        