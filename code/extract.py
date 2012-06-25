#! /usr/bin/env python-32

from os import listdir
import matplotlib as mpl 
mpl.use('cocoaagg') 
import matplotlib.pyplot as plt
import re

def main():
    path = '/Users/hs454/Desktop/tmp/'
    runs = sorted(listdir (path))
    total = []
    avg = []
    avg_all=[]
    pattern = re.compile("return_[0-9]*")
    bucket = []
    for run in runs:
        if pattern.match(run):
            speeds=[]
            f = open(run)
            lines = f.readlines()
            for line in lines:
                spd_tr= line.split()
                ts= (int(spd_tr[1]),float(spd_tr[0])*(14.0/12))
                speeds.append(ts)
            speeds=sorted(list(set(sorted(speeds))))
            total.append(speeds)
            print speeds[0]
            max_p = speeds[-1]
            print max_p
    for i in range(0,300):
        mean = (list(total[0][i])[1]+list(total[1][i])[1]+list(total[2][i])[1])/3
        avg.append(mean)
        avg_all.append((mean,i))
        
    best = 0
    best_index=0
    for x,ii in avg_all:
        if best < x:
            best = x
            best_index = ii
    
    plt.plot(range(1,len(avg)+1), avg)
    plt.ylabel('AVERAGE SPEED')
    plt.xlabel('Trial')
    plt.annotate('global max: '+str(best), xy=(best_index,best), xytext=(best_index+15, best+0.25),arrowprops=dict(facecolor='black', shrink=0.05))
    plt.show()

if __name__ == '__main__':
	main();
