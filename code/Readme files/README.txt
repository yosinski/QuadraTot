Here's how to compile this sketch and upload it to the robot:

(concrete steps that could be followed by an undergrad with no robotics experience)

1. Download Arduino from the Arduino website. Install it by following all the default options.
2. Install the following code from our Git repository into your sketchbook directory. If you are using Windows, your sketchbook is likely located in your "My Documents" folder.
"My Documents\Arduino\libraries\*"
"My Documents\Arduino\hardware\*"
"My Documents\Arduino\sketches\*"
3. Open Arduino. File->Sketchbook->sketches->mainInterface.
4. In Arduino, go to Tools->Board->ArbotiX.
5. Attach the FTDI cable to the ArbotiX and your computer's USB port. Open your computer's Device Manager. Find the "Ports (COM & LTP)" section. Figure out which COM port your computer is using for the FTDI chip. Now, select this COM port in Arduino by following Tools->Ports->COM X.
6. In Arduino, click the Upload button. After about 10 seconds, you should see "Upload complete."



Here's a "Hello World" Python program showing how to move the servos in a sin wave. Before running this program, make sure you replace "COM6" with the COM port your computer uses to communicate with Aracna:

import RobotRex

robot = RobotRex(8, "COM6", cmdRate = 14)
pi = math.pi
dur = 100.0

f1 = lambda t: (abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)),
				abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)),
				abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)),
				abs(270.0*sin(10*pi*t/dur)),abs(270.0*sin(10*pi*t/dur)))
sleep(2)

robot.interpMove2(f1,f1,dur)




Here are the steps to get the HelloWorld.py program to command the robot:

1. Follow the steps above to upload "mainInterface.ino" to the ArbotiX board.
2. Unplug and replug your FTDI cable from your computer to allow a new program to access the COM Port.
3. Run python HelloWorld.py. Make sure that your python interpreter knows where to find the RobotRex file for the import to work. The robot should move!