#! /usr/bin/env python-32

from os import listdir
import matplotlib as mpl 
mpl.use('cocoaagg') 
import matplotlib.pyplot as plt
import re

def main():
    path = '/Users/hs454/Desktop/tmp/input.txt'
    f= open(path)
    lines = f.readlines()
    t = []
    j1 = []
    j2 = []
    j3 = []
    j4 = []
    j5 = []
    j6 = []
    j7 = []
    j8 = []
    for line in lines:
        joints = line.split()
        t.append(float(joints[0])-1)
        j1.append(float(joints[1]))
        j2.append(float(joints[2]))
        j3.append(float(joints[3]))
        j4.append(float(joints[4]))
        j5.append(float(joints[5]))
        j6.append(float(joints[6]))
        j7.append(float(joints[7]))
        j8.append(float(joints[8]))
    
    
    plt.plot(t,j1,'r', t,j2,'b', t,j3,'g', t,j4,'k', t,j5,'c', t,j6,'m', t,j7,'y', t,j8, 'g^')
    plt.ylabel('Motor Position')
    plt.xlabel('Time(s)')
    plt.show()
    
if __name__ == '__main__':
	main();
