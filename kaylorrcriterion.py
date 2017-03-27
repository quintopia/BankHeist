import sys
import ast
def get_bank(bettors,credits):
    selector = bettors+int(credits/100000.)
    if selector>80:
        return (.324,1.95)
    if selector>60:
        return (.387,1.65)
    if selector>40:
        return (.425,1.3)
    if selector>20:
        return (.488,1.1)
    return (.54,.8)

game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,p,b,myyattas,mybet,mypayment,bank0,bank1,bank2,bank3,bank4,myrank,mu_yattas,sigma_yattas,max_yattas = map(ast.literal_eval,sys.argv[1:])

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
    if alreadyplayed < 0.37*numbet or numbet==0:
        print "!guncheck"
    else:
        realp = p*numready/float(alreadyplayed)
        f = (realp*(b+1)-(1-240./(myyattas+240.)))/b
        print "!guncheck" if f>0 else "back out"
    