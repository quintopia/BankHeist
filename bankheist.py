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
def rabblebot(game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,p,b,myyattas,mybet,mypayment,bank_holdings,rank,mu_yattas,sigma_yattas,max_yattas,errors):
    if round==2:
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
    msg = " ".join(map(str,args[:14]))+" "+" ".join(map(str,args[14]))+" "+" ".join(map(str,args[15:-1]))
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
    
    def do_payment(self,bonus):
        if not self.hired and random.randint(1,20)==20:
            self.payment*=1.5
            self.hired = True
        if self.hired:
            self.yattas += self.payment
        self.yattas += bonus
        
    def update(self,bankid,p,dcsuccess):
        basep = self.bankprobs[bankid]
        p = p*basep
        b = self.bankodds[bankid]
        dcreturnval = 0
        if self.decision == "all in":
                if random.random()<basep:
                    self.yattas = int(b*(self.yattas+240))
                else:
                    self.yattas = 0
        else:
            if random.random()<p:
                self.yattas -= self.bet
                winnings = int((b+1)*self.bet)
                if self.decision == "acquire intel":
                    self.bankodds[bankid] += .00001*winnings
                    winnings = 0
                elif self.decision == "deposit":
                    self.bankholdings[bankid] += winnings
                    winnings = 0
                elif self.decision == "withdraw":
                    winnings += self.bankholdings[bankid]
                    self.bankholdings[bankid] = 0
                if dcsuccess and self.decision != "double cross":
                    dcreturnval = winnings
                    winnings = 0
                self.yattas += winnings
            else:
                self.yattas -= self.bet
        if self.decision == "buy guard":
            self.payment -= 1
            self.bankprobs[bankid] += .01*(1-bankprobs[bankid])
        if self.decision == "change jobs":
            self.hired = False
        if self.decision not in ["back out","all in"] and self.hired:
            self.yattas += self.payment
        else:
            self.decision = "stick"
        for i in range(5):
            self.bankholdings[i] += int(0.0014*self.bankholdings[i])
        return dcreturnval
    
    def decide(self,game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,mu_yattas,sigma_yattas,max_yattas,errors):
        p = self.bankprobs[bankid]
        b = self.bankodds[bankid]
        try:
            if round == 1:
                #game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,p,b,myyattas,mybet,mypayment,bank_holdings,rank,mu_yattas,sigma_yattas,max_yattas,errors
                self.bet = max(0,min(self.yattas,int(self.function(game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,p,b,self.yattas,0,self.payment,self.bankholdings,self.rank,mu_yattas,sigma_yattas,max_yattas,errors))))
            else:
                self.decision = self.function(game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,p,b,self.yattas,self.bet,self.payment,self.bankholdings,self.rank,mu_yattas,sigma_yattas,max_yattas,errors)
        except Exception as e:
            errors.write(str(e)+"\n")
            self.bet = 0
            self.decision = "stick"
            pass

def rungame(players,rounds,logfile,errors):
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
        realstickers = 0
        backstabbers = []
        for i,player in enumerate(bettors):
            #game,round,numplayers,alreadyplayed,numbet,yattasbet,numready,bankid,mu_yattas,sigma_yattas,max_yattas,errors
            player.decide(game,2,len(bettors),i,len(bettors),investment,stickers,bankid,mu_yattas,sigma_yattas,max_yattas,errors)
            if player.decision == "back out":
                player.bet = 0
            else:
                stickers += 1
                if player.name != "rabble":
                    realstickers += 1
            if player.decision == "double cross":
                backstabbers.append(player)
            if player.name != "rabble":
                logfile.write("%s decided to %s.\n"%(player.name,player.decision))
        #compute results
        if len(bettors):
            p = stickers/len(bettors)
        else:
            p=0
        dcsuccess = len(backstabbers) <= realstickers/10
        dcjackpot = 0
        for player in players:
            dcjackpot += player.update(bankid,p,dcsuccess)
        for player in players:
            bonus = dcjackpot/max(1,len(backstabbers))
            player.do_payment(bonus if player in backstabbers else 0)
        realplayers.sort(key=lambda p: -p.yattas)
        logfile.write("\nResults:\n")
        for i,player in enumerate(realplayers):
            logfile.write("%d. %s: %d\n"%(i,player.name,player.yattas))
        logfile.write("\n\n")
    print_progress(rounds,rounds)
    return [(player.name,player.yattas) for player in realplayers]
                
if __name__=="__main__":
    import os
    players = []
    with open("competitors.txt") as f:
        for line in f:
            parts = line.split(" ")
            name = parts[0]
            command = " ".join(parts[1:]).strip()
            players.append((name,command))
    with open("log.txt","w") as logfile:
        with open("errors.txt","w") as errors:
            results = rungame(players,random.randint(10,11),logfile,errors)
    with open("results.txt","w") as f:
        f.write(tabulate(results,headers=["Program Name","Final Score"]))