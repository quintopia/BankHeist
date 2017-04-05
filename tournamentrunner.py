import sys
import bankheist
import time
from collections import defaultdict as ddict

players = []
rounds = 1000
with open("competitors.txt") as f:
    for line in f:
        if line.startswith("#"): continue
        parts = line.split(" ")
        name = parts[0]
        command = " ".join(parts[1:]).strip()
        players.append((name,command))
scores = ddict(int)
with open("log.txt","w") as logfile:
    with open("errors.txt","w") as errors:
        starttime = time.time()
        tourneycount = 1
        while time.time()-starttime < 24*3600:
            logfile.write("!#$&%^*$!&#^%*&%^$!#* Tournment #%d !@(#&^*$(*!^&#@$%(*^!&\n\n"%tourneycount
            tourneycount+=1
            results = bankheist.rungame(players,random.randint(rounds,int(1.1*rounds)),logfile,errors,False)
            bankheist.print_progress(time.time()-starttime,24*3600)
            for player,yattas in result:
                scores[player]+=yattas
with open("results.txt","w") as f:
    f.write(tabulate(scores.items(),headers=["Program Name","Final Score"]))
