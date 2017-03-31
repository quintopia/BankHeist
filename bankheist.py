# -*- coding: utf-8 -*-
import subprocess
import random
import functools
import sys
from tabulate import tabulate

def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def get_bank(bettors,credits):
    selector = bettors+int(credits/100000.)
    return min(4,int(selector/20.))
    
    #game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,self.yattas,0,self.payment,self.bankholdings,self.rank,mu_yattas,sigma_yattas,max_yattas,errors
def rabblebot(game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,myyattas,mybet,mypayment,hired,rank,mu_yattas,sigma_yattas,max_yattas,bank_holdings,bankprobs,bankodds,errors):
    p = bankprobs[bankid]
    if round==2:
        if alreadyplayed and random.random()<0.55-0.5*numready/alreadyplayed:
            return "back out"
        else:
            return "!guncheck"
    if random.random()>p:
        return 0
    else:
        if myyattas>80085:
            return 80085
        elif myyattas>6969:
            return 6969
        elif myyattas>420:
            return 420
        else:
            return 69
def outsideplayer(*args):
    errors = args[-1]
    msg = " ".join(map(str,args[:-4]))+" "+" ".join(map(str,args[-4]+args[-3]+args[-2]))
    result = subprocess.check_output(msg,stderr=errors,shell=True).strip()
    return result
    
class Bot:
    def __init__(self,name,function):
        self.yattas = 240
        self.function = function
        self.bet = 0
        self.decision = "stick"
        self.name = name
        self.rank = 1
        self.payment = 240
        self.hired = True
        self.bankholdings = [0]*5
        self.bankprobs = [0.54,0.488,0.425,0.387,0.324]
        self.bankodds = [0.8,1.1,1.3,1.65,1.95]
        self.fingered = False
        self.fingersuccess = False
        self.winnings = 0
        self.guardbribes = []
    
    def do_payment(self,dcsuccess,dcwinnings,straightwinnings):
        if self.decision == "double cross" and (not dcsuccess or self.fingered):
            self.payment/=2
            self.hired = False
            self.winnings = 0
        if not self.hired and random.randint(1,20)==20:
            self.payment+=int(self.payment/10)
            self.hired = True
        if self.decision not in ["back out","all in"] and self.hired:
            self.yattas += self.payment
        if self.decision == "double cross" and dcsuccess and not self.fingered:
            self.yattas += self.winnings + dcwinnings
        elif self.decision == "finger" and not dcsuccess and self.fingersuccess:
            self.yattas += self.winnings/2
        elif not dcsuccess:
            self.yattas += self.winnings
        if self.decision not in ["back out","all in","double cross"] and not dcsuccess and (self.fingersuccess or not self.decision == "finger"):
            self.yattas += straightwinnings
        self.yattas -= len(self.guardbribes)
        if self.yattas < 0:
            random.shuffle(self.guardbribes)
            for i in range(-self.yattas):
                bankid = self.guardbribes.pop()
                self.bankprobs[bankid] = (self.bankprobs[bankid]-0.01)/0.99
            self.yattas=0
        self.winnings = 0
        self.bet = 0 #just to be sure :D
        self.fingered = False
        self.fingersuccess = False
        self.decision = "stick"
        
    def update(self,bankid,p,dcsuccess,heisters):
        basep = self.bankprobs[bankid]
        p = p*basep
        b = self.bankodds[bankid]
        if self.decision == "all in":
                if random.random()<basep:
                    self.yattas = int(b*(self.yattas+240))
                else:
                    self.yattas = 0
        else:
            self.yattas -= self.bet
            if random.random()<p:
                self.winnings = int((b+1)*self.bet)
                if self.decision == "acquire intel":
                    self.bankodds[bankid] += .00001*self.winnings
                    self.winnings = 0
                elif self.decision == "deposit":
                    self.bankholdings[bankid] += self.winnings
                    self.winnings = 0
                elif self.decision == "withdraw":
                    self.winnings += self.bankholdings[bankid]
                    self.bankholdings[bankid] = 0
                if self.decision == "finger":
                    for i in range(10):
                        test = random.choice(heisters)
                        if test.decision == "double cross" and not test.fingered:
                            test.fingered = True
                            self.fingersuccess = True
                            pmt = test.yattas/4
                            test.yattas-=pmt
                            test.bankprobs[bankid]-=0.05
                            self.yattas+=pmt
                    if not self.fingersuccess:
                        self.bankodds[bankid]-=0.05
            if self.decision == "buy guard":
                self.guardbribes.append(bankid)
                self.bankprobs[bankid] += .01*(1-self.bankprobs[bankid])
            if self.decision == "change jobs":
                self.hired = False
        for i in range(5):
            self.bankholdings[i] += int(0.0014*self.bankholdings[i])
        if self.decision=="finger" and not self.fingersuccess:
            return self.winnings/2
        elif (dcsuccess and (self.decision not in ["all in","back out"] or self.fingered)) or (self.decision=="double cross" and (not dcsuccess or self.fingered)):
            return self.winnings
        else:
            return 0
    
    def decide(self,game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,mu_yattas,sigma_yattas,max_yattas,errors):
        p = self.bankprobs[bankid]
        b = self.bankodds[bankid]
        try:
            if round == 1:
                #game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,p,b,myyattas,mybet,mypayment,bank_holdings,rank,mu_yattas,sigma_yattas,max_yattas,errors
                self.bet = max(0,min(self.yattas,int(self.function(game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,self.yattas,0,self.payment,int(self.hired),self.rank,mu_yattas,sigma_yattas,max_yattas,self.bankholdings,self.bankprobs,self.bankodds,errors))))
            else:
                self.decision = self.function(game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,self.yattas,self.bet,self.payment,int(self.hired),self.rank,mu_yattas,sigma_yattas,max_yattas,self.bankholdings,self.bankprobs,self.bankodds,errors)
        except Exception as e:
            errors.write(str(e)+"\n")
            self.bet = 0
            self.decision = "stick"
            pass

def rungame(players,rounds,logfile,errors,verbose=True):
    #set up real players
    realplayers = []
    for i in range(len(players)):
            realplayers.append(Bot(players[i][0],functools.partial(outsideplayer,players[i][1])))
    #set up rabble
    rabble = []
    for i in range(500):
        rabble.append(Bot("rabble",rabblebot))
    for game in range(rounds):
        print_progress(game,rounds)
        #compute distribution stats
        #compute ranks
        prev = realplayers[0]
        realplayers[0].rank=1
        for i,player in enumerate(realplayers[1:]):
            if player.yattas == prev.yattas:
                player.rank = prev.rank
            else:
                player.rank = i+2
        #compute mean
        mu_yattas = int(sum([player.yattas for player in realplayers])/float(len(realplayers)))
        #compute MAD
        sigma_yattas = int(sum([abs(player.yattas-mu_yattas) for player in realplayers])/float(len(realplayers)))
        #compute max
        max_yattas = realplayers[0].yattas
        #create array of players
        players = []
        players.extend(realplayers) #copy realplayers
        #add in rabble
        numrabble = random.randint(0,500)
        players.extend(random.sample(rabble,numrabble))
        numplayers = len(players)
        logfile.write("#####GAME %d: %d players######\n"%(game,numplayers))
        #do round 1
        logfile.write("\nRound 1:\n")
        bettors = []
        investment = 0
        random.shuffle(players)
        for i,player in enumerate(players):
            #game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,mu_yattas,sigma_yattas,max_yattas,errors
            player.decide(game,1,numplayers,i,len(bettors),investment,0,get_bank(len(bettors),investment),mu_yattas,sigma_yattas,max_yattas,errors)
            investment+=player.bet
            if player.bet>0:
                bettors.append(player)
            if player.name != "rabble":
                logfile.write("%s bet %d.\n"%(player.name,player.bet))
        #do round 2
        logfile.write("\nRound 2\n")
        bankid = get_bank(len(bettors),investment)
        random.shuffle(bettors)
        stickers = 0
        realstickers = []
        backstabbers = []
        numstraight = 0
        for i,player in enumerate(bettors):
            #game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,mu_yattas,sigma_yattas,max_yattas,errors
            player.decide(game,2,len(bettors),i,len(bettors),investment,stickers,bankid,mu_yattas,sigma_yattas,max_yattas,errors)
            if player.decision == "back out":
                player.bet = 0
            else:
                stickers += 1
                if player.name != "rabble":
                    realstickers.append(player)
                if player.decision == "double cross":
                    backstabbers.append(player)
                elif player.decision!="all in":
                    numstraight += 1
            if player.name != "rabble":
                logfile.write("%s decided to %s.\n"%(player.name,player.decision))
        #compute results
        if len(bettors):
            p = stickers/len(bettors)
        else:
            p=0
        dcsuccess = len(backstabbers)==1 or 0 < len(backstabbers) <= len(realstickers)/10
        pot = 0
        for player in players:
            pot+=player.update(bankid,p,dcsuccess,realstickers)
        successfulbackstabbers = filter(lambda p:not p.fingered,backstabbers)
        dcwinnings = 0
        if dcsuccess:dcwinnings = len(successfulbackstabbers)*pot/len(backstabbers)
        straightwinnings = (len(backstabbers)-len(successfulbackstabbers))*pot/numstraight
        for player in players:
            player.do_payment(dcsuccess,dcwinnings,straightwinnings)
        realplayers.sort(key=lambda p: -p.yattas)
        logfile.write("\nResults:\n")
        for i,player in enumerate(realplayers):
            logfile.write("%d. %s: %d\n"%(i,player.name,player.yattas))
        logfile.write("\n\n")
    if verbose: print_progress(rounds,rounds)
    return [(player.name,player.yattas) for player in realplayers]
                
if __name__=="__main__":
    players = []
    rounds = int(sys.argv[1])
    with open("competitors.txt") as f:
        for line in f:
            parts = line.split(" ")
            name = parts[0]
            command = " ".join(parts[1:]).strip()
            players.append((name,command))
    with open("log.txt","w") as logfile:
        with open("errors.txt","w") as errors:
            results = rungame(players,random.randint(rounds,int(1.1*rounds)),logfile,errors)
    with open("results.txt","w") as f:
        f.write(tabulate(results,headers=["Program Name","Final Score"]))