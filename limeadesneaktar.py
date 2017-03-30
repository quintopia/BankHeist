import sys
import ast

game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,myyattas,mybet,mypayment,hired,myrank,mu_yattas,sigma_yattas,max_yattas = map(ast.literal_eval,sys.argv[1:17])
bankholdings = map(int,sys.argv[17:22])
bankprobs = map(float,sys.argv[22:27])
bankodds = map(float,sys.argv[27:32])

if round==1:
    print 1
else:
    if hired and game<900:
        print "change jobs"
    else:
        print "double cross"