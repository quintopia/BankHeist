import sys
import ast
game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,myyattas,mybet,mypayment,hired,myrank,mu_yattas,sigma_yattas,max_yattas = map(ast.literal_eval,sys.argv[1:17])
bankholdings = map(int,sys.argv[17:22])
bankprobs = map(float,sys.argv[22:27])
bankodds = map(float,sys.argv[27:32])

def get_bank(bettors,credits):
    selector = min(4,int(bettors+int(credits/100000.)/20))
    return bankprobs[selector],bankodds[selector]

if round == 1:
    if alreadyplayed < 0.37*numplayers or numbet==0:
        print 0
        #sys.stderr.write("1: %d,%d\n"%(alreadyplayed,numbet))
    else:
        ratiosofar = numbet/float(alreadyplayed)
        bettors = ratiosofar * numplayers
        ratesofar = yattasbet/float(numbet)
        credits = bettors*ratesofar
        p,b = get_bank(bettors,credits)
        f = (p*(b+1)-1)/b
        print max(int(f*myyattas),0)
        #sys.stderr.write("2: %d,%d\n"%(p,b))
else:
    print "!gunHeCK"
    