#! /usr/bin/env python

import cwiid
import sys
import threading
import socket
import random
from datetime import datetime
from time import sleep

USAGE = '''wmtracker.py [options] port

port is required

Options:
   -f Skip connecting to wiimote, send fake random data instead.

Example:
   ./wmtracker.py 8080'''

# where to serve the tracking information
HOST = 'localhost'
#PORT = 8080
MSGLENGTH = 32

menu = '''Wii demo commands:
  1: toggle LED 1
  2: toggle LED 2
  3: toggle LED 3
  4: toggle LED 4
  5: toggle rumble
  a: toggle accelerometer reporting
  b: toggle button reporting
  c: enable motionplus, if connected
  e: toggle extension reporting
  i: toggle ir reporting
  m: toggle messages
  p: print this menu
  r: request status message ((o) enables callback output)
  s: print current state
  o: toggle status reporting
  x: exit

Tracking commands:
  t: toggle tracking'''



def pad(string, padto = MSGLENGTH):
    return '%-32s' % string

class ServerThread (threading.Thread):
    def __init__(self, port, fakeMode = False):
        threading.Thread.__init__(self)
        self.port     = port
        self.fakeMode = fakeMode
        self.pushConn = None
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def keepRunning(self):
        return not self._stop.isSet()

    def run(self):
        print 'Server thread started'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, self.port))
        print 'Listening for connection on %s:%d' % (HOST, self.port)
        s.settimeout(1.0)   # 1 second timeout
        conn = None
        while self.keepRunning():
            s.listen(3)
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue
            print 'Connected by', addr

            while self.keepRunning():
                try:
                    data = conn.recv(256)         # This still blocks, even with timeout :-/
                except:
                    # connection reset by peer, relisten
                    break

                if not data:
                    print 'Connection lost, listening for new connection on %s:%d' % (HOST, self.port)
                    break

                print 'Received %s' % repr(data),
                #conn.send(datetime.now().ctime())
                #conn.send(repr(wiimote.state))

                if data == '-':
                    if self.fakeMode:
                        st = 'P:%04d:%04d' % (random.uniform(0,1023), random.uniform(0,766))
                    else:
                        if not ('ir_src' in wiimote.state):
                            st = 'E:No wiimote state?'
                        elif wiimote.state['ir_src'][0] is None:
                            st = 'E:No targets'
                        elif wiimote.state['ir_src'][2] is not None:
                            st = 'E:More than one target'
                        else:
                            xy = wiimote.state['ir_src'][0]['pos']
                            st = 'P:%04d:%04d:' % (xy[0], xy[1])
                    send = pad(st)
                    conn.send(send)
                    print 'Sent%s: "%s"' % (' FAKE DATA' if self.fakeMode else '', send)
                elif data == 's':
                    self.pushConn = conn
                else:
                    print 'Error: do not know what to do with "%s"' % data
                    continue
        if conn:
            conn.close()
        s.close()
        print 'Server thread done.'

    def pushCallback(self, wiimote):
        '''Called whenever wiimote state is updated'''
        #print 'got push!'
        if self.pushConn is not None:
            #print 'have pushConn'
            if not ('ir_src' in wiimote.state):
                st = 'E:No wiimote state?'
            elif wiimote.state['ir_src'][0] is None:
                st = 'E:No targets'
            elif wiimote.state['ir_src'][2] is not None:
                st = 'E:More than one target'
            else:
                xy = wiimote.state['ir_src'][0]['pos']
                st = 'P:%04d:%04d:' % (xy[0], xy[1])
            send = pad(st)
            try:
                self.pushConn.send(send)
                #print 'Sent%s: "%s"' % (' FAKE DATA' if self.fakeMode else '', send)
            except socket.error:
                print 'Socket error (connection lost?), dropping pushConn'
                self.pushConn = None
            
        else:
            #print 'self.pushConn is None, skipping push'
            pass



def main():
    led = 0
    rpt_mode = 0
    rumble = 0
    mesg = False
    trackOn = False



    fakeMode = False
    if len(sys.argv) == 1:
        print USAGE
        exit(1)
    if sys.argv[1] == '-f':
        fakeMode = True
        #Connect to address given on command-line, if present
        #wiimote = cwiid.Wiimote(sys.argv[1])
        #wiimote = cwiid.Wiimote()
        del sys.argv[1]
    if len(sys.argv[1]) == 1:
        print USAGE
        exit(1)
    try:
        port = int(sys.argv[1])
    except:
        print 'Bad port'
        exit(1)

    if fakeMode:
        print 'FAKE MODE: server will send fake data'
    else:
        print 'Put Wiimote in discoverable mode now (press 1+2)...'
        global wiimote
        wiimote = cwiid.Wiimote()
        wiimote.mesg_callback = callback

    print menu

    doExit = 0
    while not doExit:
        c = sys.stdin.read(1)
        if c == '1':
            led ^= cwiid.LED1_ON
            wiimote.led = led
        elif c == '2':
            led ^= cwiid.LED2_ON
            wiimote.led = led
        elif c == '3':
            led ^= cwiid.LED3_ON
            wiimote.led = led
        elif c == '4':
            led ^= cwiid.LED4_ON
            wiimote.led = led
        elif c == '5':
            rumble ^= 1
            wiimote.rumble = rumble
        elif c == 'a':
            rpt_mode ^= cwiid.RPT_ACC
            wiimote.rpt_mode = rpt_mode
        elif c == 'b':
            rpt_mode ^= cwiid.RPT_BTN
            wiimote.rpt_mode = rpt_mode
        elif c == 'c':
            wiimote.enable(cwiid.FLAG_MOTIONPLUS)
        elif c == 'e':
            rpt_mode ^= cwiid.RPT_EXT
            wiimote.rpt_mode = rpt_mode
        elif c == 'i':
            rpt_mode ^= cwiid.RPT_IR
            wiimote.rpt_mode = rpt_mode
        elif c == 'm':
            mesg = not mesg
            if mesg:
                wiimote.enable(cwiid.FLAG_MESG_IFC);
            else:
                wiimote.disable(cwiid.FLAG_MESG_IFC);
        elif c == 'p':
            print menu
        elif c == 'r':
            wiimote.request_status()
        elif c == 's':
            print_state(wiimote.state)
        elif c == 'o':
            rpt_mode ^= cwiid.RPT_STATUS
            wiimote.rpt_mode = rpt_mode
        elif c == 'x':
            doExit = -1;

        elif c == 't':
            trackOn = not trackOn
            if not fakeMode:
                rpt_mode ^= cwiid.RPT_IR
                #rpt_mode ^= cwiid.RPT_STATUS
                wiimote.rpt_mode = rpt_mode
            if trackOn:
                serverThread = ServerThread(port, fakeMode)
                serverThread.daemon = True
                serverThread.start()
                if not fakeMode:
                    wiimote.mesg_callback = lambda mesg_list,time : track_callback(mesg_list, time, serverThread.pushCallback)
                    wiimote.enable(cwiid.FLAG_MESG_IFC)
            else:
                serverThread.stop()
                print 'Waiting for server thread to quit...',
                while serverThread.isAlive():
                    print '.',
                    sys.stdout.flush()
                    sleep(.5)
                serverThread.join()
                print 'done.'
                if not fakeMode:
                    wiimote.mesg_callback = callback
                    wiimote.disable(cwiid.FLAG_MESG_IFC);
                
        elif c == '\n':
            pass
        else:
            print 'invalid option'

    if not fakeMode:
        wiimote.close()
    print 'Shutting down.'



def print_state(state):
    print 'Report Mode:',
    for r in ['STATUS', 'BTN', 'ACC', 'IR', 'NUNCHUK', 'CLASSIC', 'BALANCE', 'MOTIONPLUS']:
        if state['rpt_mode'] & eval('cwiid.RPT_' + r):
            print r,
    print

    print 'Active LEDs:',
    for led in ['1','2','3','4']:
        if state['led'] & eval('cwiid.LED' + led + '_ON'):
            print led,
    print

    print 'Rumble:', state['rumble'] and 'On' or 'Off'

    print 'Battery:', int(100.0 * state['battery'] / cwiid.BATTERY_MAX)

    if 'buttons' in state:
        print 'Buttons:', state['buttons']

    if 'acc' in state:
        print 'Acc: x=%d y=%d z=%d' % (state['acc'][cwiid.X],
                                       state['acc'][cwiid.Y],
                                       state['acc'][cwiid.Z])

    if 'ir_src' in state:
        valid_src = False
        print 'IR:',
        for src in state['ir_src']:
            if src:
                valid_src = True
                print src['pos'],

        if not valid_src:
            print 'no sources detected'
        else:
            print

    if state['ext_type'] == cwiid.EXT_NONE:
        print 'No extension'
    elif state['ext_type'] == cwiid.EXT_UNKNOWN:
        print 'Unknown extension attached'
    elif state['ext_type'] == cwiid.EXT_NUNCHUK:
        if state.has_key('nunchuk'):
            print 'Nunchuk: btns=%.2X stick=%r acc.x=%d acc.y=%d acc.z=%d' % \
              (state['nunchuk']['buttons'], state['nunchuk']['stick'],
               state['nunchuk']['acc'][cwiid.X],
               state['nunchuk']['acc'][cwiid.Y],
               state['nunchuk']['acc'][cwiid.Z])
    elif state['ext_type'] == cwiid.EXT_CLASSIC:
        if state.has_key('classic'):
            print 'Classic: btns=%.4X l_stick=%r r_stick=%r l=%d r=%d' % \
              (state['classic']['buttons'],
               state['classic']['l_stick'], state['classic']['r_stick'],
               state['classic']['l'], state['classic']['r'])
    elif state['ext_type'] == cwiid.EXT_BALANCE:
        if state.has_key('balance'):
            print 'Balance: right_top=%d right_bottom=%d left_top=%d left_bottom=%d' % \
              (state['balance']['right_top'], state['balance']['right_bottom'],
               state['balance']['left_top'], state['balance']['left_bottom'])
    elif state['ext_type'] == cwiid.EXT_MOTIONPLUS:
        if state.has_key('motionplus'):
            print 'MotionPlus: angle_rate=(%d,%d,%d)' % state['motionplus']['angle_rate']



def callback(mesg_list, time):
    print 'time: %f' % time
    for mesg in mesg_list:
        if mesg[0] == cwiid.MESG_STATUS:
            print 'Status Report: battery=%d extension=' % \
                   mesg[1]['battery'],
            if mesg[1]['ext_type'] == cwiid.EXT_NONE:
                print 'none'
            elif mesg[1]['ext_type'] == cwiid.EXT_NUNCHUK:
                print 'Nunchuk'
            elif mesg[1]['ext_type'] == cwiid.EXT_CLASSIC:
                print 'Classic Controller'
            elif mesg[1]['ext_type'] == cwiid.EXT_BALANCE:
                print 'Balance Board'
            elif mesg[1]['ext_type'] == cwiid.EXT_MOTIONPLUS:
                print 'MotionPlus'
            else:
                print 'Unknown Extension'

        elif mesg[0] == cwiid.MESG_BTN:
            print 'Button Report: %.4X' % mesg[1]

        elif mesg[0] == cwiid.MESG_ACC:
            print 'Acc Report: x=%d, y=%d, z=%d' % \
                  (mesg[1][cwiid.X], mesg[1][cwiid.Y], mesg[1][cwiid.Z])

        elif mesg[0] == cwiid.MESG_IR:
            valid_src = False
            print 'IR Report: ',
            for src in mesg[1]:
                if src:
                    valid_src = True
                    print src['pos'],

            if not valid_src:
                print 'no sources detected'
            else:
                print

        elif mesg[0] == cwiid.MESG_NUNCHUK:
            print ('Nunchuk Report: btns=%.2X stick=%r ' + \
                   'acc.x=%d acc.y=%d acc.z=%d') % \
                  (mesg[1]['buttons'], mesg[1]['stick'],
                   mesg[1]['acc'][cwiid.X], mesg[1]['acc'][cwiid.Y],
                   mesg[1]['acc'][cwiid.Z])
        elif mesg[0] == cwiid.MESG_CLASSIC:
            print ('Classic Report: btns=%.4X l_stick=%r ' + \
                   'r_stick=%r l=%d r=%d') % \
                  (mesg[1]['buttons'], mesg[1]['l_stick'],
                   mesg[1]['r_stick'], mesg[1]['l'], mesg[1]['r'])
        elif mesg[0] ==  cwiid.MESG_BALANCE:
            print ('Balance Report: right_top=%d right_bottom=%d ' + \
                   'left_top=%d left_bottom=%d') % \
                  (mesg[1]['right_top'], mesg[1]['right_bottom'],
                   mesg[1]['left_top'], mesg[1]['left_bottom'])
        elif mesg[0] == cwiid.MESG_MOTIONPLUS:
            print 'MotionPlus Report: angle_rate=(%d,%d,%d)' % \
                  mesg[1]['angle_rate']
        elif mesg[0] ==  cwiid.MESG_ERROR:
            print "Error message received"
            global wiimote
            wiimote.close()
            exit(-1)
        else:
            print 'Unknown Report'



def track_callback(mesg_list, time, other_callback):
    #print 'got something, time is', time
    for mesg in mesg_list:
        if mesg[0] ==  cwiid.MESG_ERROR:
            print "Error message received"
            global wiimote
            wiimote.close()
            exit(-1)
        else:
            #print 'Unknown Report'
            pass
    #print 'state is ', wiimote.state
    other_callback(wiimote)



if __name__ == '__main__':
    main()
