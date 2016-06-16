"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Update the master file with probe values every day at 2am.
"""

import threading
from datetime import datetime
import imp
import os
r1du = imp.load_source('R1datautils', os.getcwd() + '/Project/R1datautils.py')

def main():
        def update_r1_masterfile():
            # Takes relevant point from giant data file and puts in master R1 file
            x = datetime.today()
            y = x.replace(day=x.day+1, hour=2, minute=0, second=0, microsecond=0)
            delta_t = y-x
            secs = delta_t.seconds+1
            print ('Updating master file...')
            r1du.populate_r1masterfile()
            threading.Timer(secs, update_r1_masterfile).start()
            print ('Done')
        update_r1_masterfile()
main()