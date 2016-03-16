"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Read reactor data to google drive every 30 secs.
"""

import sched
import time
from googledriveutils import write_to_reactordrive

s = sched.scheduler(time.time, time.sleep)


def main(sc):
    """
    Queries reactor for latest data and appends to google drive file every 30s.
    :param sc: run again.
    :return:
    """
    print 'Querying Reactor'
    write_to_reactordrive(1, 'R1data')
    sc.enter(30, 1, main, (sc,))

s.enter(30, 1, main, (s,))
s.run()
