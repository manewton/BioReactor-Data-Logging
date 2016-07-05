"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Update the master file with probe values every day at 2am.
"""

import schedule
import time
import imp
import os
r1du = imp.load_source('R1datautils', os.getcwd() + '/Project/R1datautils.py')

# Takes relevant point from giant data file and puts in master R1 file
schedule.every().day.at("02:00").do(r1du.populate_r1masterfile())

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute