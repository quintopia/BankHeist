import sys
import ast
import random

game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,myyattas,mybet,mypayment,hired,myrank,mu_yattas,sigma_yattas,max_yattas = map(ast.literal_eval,sys.argv[1:17])
bankholdings = map(int,sys.argv[17:22])
bankprobs = map(float,sys.argv[22:27])
bankodds = map(float,sys.argv[27:32])

if round == 1:
    if game<800:
        print 69
    else:
        print myyattas/4
else:
    if game<800:
        if hired:
            print "change jobs"
        else:
            print random.choice(["acquire intel","buy guard"])
    else:
        if myrank>1:
            print "all in"
        else:
            print "!guncheck"
    