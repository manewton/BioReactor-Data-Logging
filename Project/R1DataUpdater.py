"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Update the master file with probe values every day at 2am.
"""

import threading
from R1datautils import populate_r1masterfile
from datetime import datetime


def main():
        # Takes relevant point from giant data file and puts in master R1 file
        x = datetime.today()
        y = x.replace(day=x.day+1, hour=2, minute=0, second=0, microsecond=0)
        delta_t = y-x
        secs = delta_t.seconds+1
        threading.Timer(secs, populate_r1masterfile).start()

main()
