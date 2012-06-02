#! /usr/bin/env python-32

from os import listdir
import matplotlib as mpl 
mpl.use('cocoaagg') 
import matplotlib.pyplot as plt
import re
import numpy as np

def main():
    path = '/Users/hs454/Desktop/tmp/'
    runs = sorted(listdir (path))
    total = []
    best1_all = []
    best2_all = []
    best3_all = []
    avg_all=[]
    avg=[]
    stds=[]
    upper=[]
    lower=[]
    pattern = re.compile("return_[0-9]*")
    bucket = []
    best1 = 0
    best2 = 0
    best3 = 0
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

    for i in range(0,300):
        e1 = list(total[0][i])[1]
        e2 = list(total[1][i])[1]
        e3 = list(total[2][i])[1]
        if best1 < e1:
            best1=e1
        if best2 < e2:
            best2=e2
        if best3 < e3:
            best3=e3
        std = np.std([best1,best2,best3])
        stds.append(std)
        best1_all.append(best1)
        best2_all.append(best2)
        best3_all.append(best3)
        mean = (best1+best2+best3)/3
        avg.append(mean)
        upper.append(mean+std)
        lower.append(mean-std)
        avg_all.append((mean,i))
        
    maxi = max([best1,best2,best3])
    print 'global max ',maxi
    std = np.std(avg)
    print 'standard deviation: ', std
    plt.plot(range(1,len(avg)+1), avg, 'b', range(1,len(avg)+1),upper,'g', range(1,len(avg)+1), lower,'r')
    plt.ylabel('Speed(cm/sec)')
    plt.xlabel('Trial')
    plt.savefig('average.pdf')
    #plt.show()

if __name__ == '__main__':
	main();
