import sys
import ast
import random
game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,myyattas,mybet,mypayment,hired,myrank,mu_yattas,sigma_yattas,max_yattas = map(ast.literal_eval,sys.argv[1:17])
bankholdings = map(int,sys.argv[17:22])
bankprobs = map(float,sys.argv[22:27])
bankodds = map(float,sys.argv[27:32])

if round ==1:
    if game < 900:
        print myyattas/10
    elif sum(bankholdings)>0:
        print 1
    else:
        print 0
else:
    if game < 500 and hired:
        print random.choice(["change jobs","finger"])
    elif game < 900:
        print "deposit"
    elif bankholdings[bankid]>0:
        print "withdraw"
    else:
        print "!guncheck"
