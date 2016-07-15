"""
Written By: Kathryn Cogert
For: Winkler Lab cRIO bioreactors
Purpose: Read reactor data to google drive every 30 secs for R2.
"""

import threading
import imp
import os
gdu = imp.load_source('googledriveutils', os.getcwd() + '/Project/googledriveutils.py')

def main():
    """
    Saves data in google drive.
    :return:
    """
    # Timing parameters for user to inpurt
    collect_int = input('R2 data collection interval in secs: ')
    file_length = input('R2 days to wait before making new file: ')

    def r2_fromreactor():
        # Takes data from cRIO and puts it in google drive
        print 'Querying Reactor #2'
        gdu.write_to_reactordrive(2, collect_int, file_length)
        threading.Timer(collect_int, r2_fromreactor).start()

    r2_fromreactor()


main()
