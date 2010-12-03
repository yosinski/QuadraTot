A description of the files:

optimize.py: Determines a strategy to try and runs the robot with that strategy.

RunManager.py: Deals with all the details of running the robot, including choosing
an initial parameter, running the robot multiple times, tracking distance walked, and
writing to the log file. Also includes the explore dimensions method.

Strategy.py: Contains all the different possible strategies, which will be passed as
objects in optimize.py.

Robot.py: Implements the Robot class, described in Section ??.

SineModel.py: Implements a sine based motion model, described in Section ??.

Motion.py: Motion helper functions.

WiiTrackServer.py: Broadcasts the position of the infrared LED¿

WiiTrackClient.py: Connects to the WiiTrackServer to get the current position
information.