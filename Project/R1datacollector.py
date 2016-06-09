"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Read reactor data to google drive every 30 secs.
"""

import threading
from googledriveutils import write_to_reactordrive
from R1datautils import populate_r1masterfile
from datetime import datetime


def main():
    """
    Saves data in google drive.
    :return:
    """
    # Timing parameters for user to inpurt
    collect_int = input('R1 data collection interval in secs: ')
    file_length = input('R1 days to wait before making new file: ')

    def r1_fromreactor():
        # Takes data from cRIO and puts it in google drive
        print 'Querying Reactor #1'
        write_to_reactordrive(1, collect_int, file_length)
        threading.Timer(collect_int, r1_fromreactor).start()

    def r1_updatemasterfile():
        # Takes relevant point from giant data file and puts in master R1 file
        x = datetime.today()
        y = x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
        delta_t = y-x
        secs = delta_t.seconds+1
        threading.Timer(secs, populate_r1masterfile).start()
        print 'Querying Reactor #1 Master File'

    r1_updatemasterfile()
    r1_fromreactor()


main()
