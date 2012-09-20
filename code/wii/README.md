Wii Tracking Server and Example Client
===============

Brief documentation (more needed!):

1. Have the WiiMote handy and navigate to the WiiTrackServer (quadratot/code/wii/).

2. Run

        ./WiiTrackServer 8080

    to use port 8080. You will then be prompted to push buttons 1 and 2 and the WiiMote.

3. After a moment, the WiiMote should be discovered and a menu will be displayed. Type "s" to check battery level if desired, then type "t" and push enter to start tracking.

4. If desired, run ```./WiiTrackClient.py``` or ```./WiiTrackFastClient.py``` in a separate tab to check that data is being received.
