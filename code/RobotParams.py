'''Min and max values based on some tests.

Note that these values will avoid collisions only for each servo
individually.  More complex collisions are still possible given
certain vectors of motor position'''

MIN_INNER = 150
MAX_INNER = 770
MIN_OUTER = 30
MAX_OUTER = 940
MIN_CENTER = 512 - 180
MAX_CENTER = 512 + 180
