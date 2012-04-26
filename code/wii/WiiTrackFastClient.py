#! /usr/bin/env python

# Note: run like this:
#   ipython -pylab WiiTrackClient
# to be able to see the plot update live!

import socket
#from matplotlib.pyplot import plot, show, axis
from time import sleep
from datetime import datetime
#import random
import threading



class WiiTrackFastClient(object):
    '''Connects to a WiiTrackServer to track an IR LED.'''

    def __init__(self, host, port, showImage = False):
        self.host      = host
        self.port      = int(port)
        self.showImage = showImage

        self._listenThread = threading.Thread(
            name = 'listenThread',
            target = self._listener,
            args = (1,2,3))
        self._listenThread.daemon = True
        print 'Starting listening thread....'
        self._listenThread.start()
        print 'Started'

        #self.position = None
        #self.updateTIme = None
        self.posTime = (None, None)
        
        if self.showImage:
            from matplotlib.pyplot import *
            figure()
            self.positions = []


    def getPosition(self):
        position,updateTime = self.posTime
        if updateTime is None:
            return None
        td = datetime.now() - updateTime
        age = float(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
        if age > .5:
            return None
        return position


    def getPosAge(self):
        position,updateTime = self.posTime
        if updateTime is None:
            return (None, None)
        else:
            td = datetime.now() - updateTime
            age = float(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
            return (position, age)

    
    def _listener(self, a,b,c):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.send('s')   # send s to start streaming
        while True:
            data = sock.recv(1024)   # should only send length 32 string back

            #print 'Got data of length', len(data)

            if len(data) < 1:
                print 'Could not contact server'
                None

            if data[0] == 'E':
                # No target, or too many targets
                #print 'Server reported error:', data
                position = None
            elif data[0] == 'P':
                # good
                position = [int(st) for st in data.split(':')[1:3]]
                #position[0] += random.uniform(-40,40)
                #position[1] += random.uniform(-40,40)
            else:
                raise Exception('WiiTrackClient error')
            updateTime = datetime.now()
            self.posTime = (position, updateTime)

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

        sock.close()


def main():
    wc = WiiTrackFastClient('localhost', 8080)
    while True:
        #print wc.getPosition()
        sleep(1)
        print wc.getPosAge()
        print 'sleeping...'



if __name__ == '__main__':
    main()
