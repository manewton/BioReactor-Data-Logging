"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Update the master file with probe values every day at 2am.
"""

import schedule
import time
import imp
import os

# TODO: Fix
"""
    self._run_job(job)
  File "/home/cogerk/BioReactor-Data-Logging/cogert/local/lib/python2.7/site-packages/schedule/__init__.py", line 96, in _run_job
    ret = job.run()
  File "/home/cogerk/BioReactor-Data-Logging/cogert/local/lib/python2.7/site-packages/schedule/__init__.py", line 293, in run
    ret = self.job_func()
  File "/home/cogerk/BioReactor-Data-Logging/Project/R1datautils.py", line 225, in populate_r1masterfile
    val = get_val_from(1, ts, PROBE_DICT.get(probe))
  File "/home/cogerk/BioReactor-Data-Logging/Project/downloader.py", line 97, in get_val_from
    our_vals = get_values_from(reactorno, timestamp)
  File "/home/cogerk/BioReactor-Data-Logging/Project/downloader.py", line 43, in get_values_from
    df = read_from_reactordrive(reactorno, timestamp.date())
  File "/home/cogerk/BioReactor-Data-Logging/Project/googledriveutils.py", line 402, in read_from_reactordrive
    file_list = list_rfiles_by_date(reactorno, date)
  File "/home/cogerk/BioReactor-Data-Logging/Project/googledriveutils.py", line 295, in list_rfiles_by_date
    ts_date, datetime.datetime.min.time())-file_ts).days
UnboundLocalError: local variable 'ts_date' referenced before assignment
(cogert)cogerk@waffle:~/BioReactor-Data-Logging$

"""
r1du = imp.load_source('R1datautils', os.getcwd() + '/Project/R1datautils.py')

# Takes relevant point from giant data file and puts in master R1 file
schedule.every().day.at("02:00").do(r1du.populate_r1masterfile)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute