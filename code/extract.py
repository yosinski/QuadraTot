#! /usr/bin/env python

from os import listdir
import matplotlib.pyplot as plt
import re

def main():
    path = '/home/team/results/20120523_snd250Run/'
    trials = sorted(listdir (path))[4:]
    speeds = []
    pattern = re.compile("[0-9]{3}")
    for trial in trials:
        if pattern.match(trial):
            output = open(path + trial + '/output.txt' )
            print path, trial
            print ("processing " + trial)
            lines = output.readlines()
            length =len(lines)
            ss = []
            for ii, line in enumerate(lines):
                if ii == 1 or ii == length-1 :
                    t = line.split()
                    xy = [float(t[19]),float(t[20])]
                    ss.append(xy)
            speed = ((( (ss[1][0]-ss[0][0])/5.6)**2+( (ss[1][1]-ss[0][1])/5.6 )**2)**0.5)/12
            print speed
            if len(speeds) > 0 and speeds[len(speeds)-1]-speed > speed*5:
                speeds.append(speeds[len(speeds)-1]*0.85)
            else:
                speeds.append(speed)
            print("processing complete: "+trial)

    print len(speeds)
    plt.plot(range(1,len(speeds)+1), speeds)
    plt.ylabel('SPEED')
    plt.xlabel('Trial')
    plt.show()

if __name__ == '__main__':
	main();
