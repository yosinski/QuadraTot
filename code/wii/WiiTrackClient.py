#! /usr/bin/env python

# Note: run like this:
#   ipython -pylab WiiTrackClient
# to be able to see the plot update live!

import socket
#from matplotlib.pyplot import plot, show, axis
from time import sleep
#import random


class WiiTrackClient(object):
    '''Connects to a WiiTrackServer to track an IR LED.'''

    def __init__(self, host, port, showImage = False):
        self.host      = host
        self.port      = port
        self.showImage = showImage
        
        if self.showImage:
            from matplotlib.pyplot import *
            figure()
            self.positions = []

    def getPosition(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send('-')   # doesn't matter what we send
        data = s.recv(1024)   # should only send length 32 string back
        s.close()

        if len(data) < 1:
            print 'Could not contact server'
            None
        elif data[0] == 'E':
            # No target, or too many targets
            print 'Server reported error:', data
            return None
        elif data[0] == 'P':
            # good
            position = [int(st) for st in data.split(':')[1:3]]
            #position[0] += random.uniform(-40,40)
            #position[1] += random.uniform(-40,40)
        else:
            raise Exception('WiiTrackClient error')

        if self.showImage:
            N = 50
            self.positions.append(position)
            if len(self.positions) > N:
                del self.positions[0]
                
            hold(False)
            for ii,pos in enumerate(self.positions):
                #clr = str(float(len(self.positions)-ii)/50)
                ff = (len(self.positions)-float(ii)) / N
                #clr = (1.0, 1.0, float(ii)/50)
                clr = (ff, ff, 1.0)
                plot(pos[0], pos[1], 'o', color=clr, mec=clr, ms=10)
                hold(True)
            axis((0, 1024, 0, 768))
            draw()

        return position


def main():
    wc = WiiTrackClient('localhost', 8080)
    while True:
        print wc.getPosition()
        #sleep(.25)



if __name__ == '__main__':
    main()
