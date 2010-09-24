'''

@date: 24 September 2010

'''

"""
Given the time since the robot started running (type float?), returns a
list of length 9 that denotes the position each motor should be at
at the given time. Motors 0, 2, 4, and 6 are the lower/base motors;
1, 3, 5, and 7 are the outer motors; 8 is the motor in the center of the
robot. Motor positions are of type int, [0, 1023], 512 being lying flat.

"""

import math

def positionIt(time):
    # Make the outer arm go up and down, limited range until we figure
    # out range of robot. Starts out lying flat.
    outerMotor = int(round(512 + (238 * abs(math.sin(time)))))  # TODO: Scale time correctly?
    position = [512, outerMotor, 512, outerMotor, 512, outerMotor, 512,
                    outerMotor, 512]
    return position