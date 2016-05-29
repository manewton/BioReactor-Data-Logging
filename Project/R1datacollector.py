"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Read reactor data to google drive every 30 secs.
"""

import threading
from googledriveutils import write_to_reactordrive, find_folderid, \
    get_file_list


def main():
    """
    Queries reactor for latest data and appends to google drive file every 30s.
    :param sc: run again.
    :return:
    """
    collect_int = input('R1 data collection interval in secs: ')
    file_length = input('R1 days to wait before making new file: ')
    def R1_collect():
        write_to_reactordrive(1, collect_int, file_length)
        print 'Querying Reactor #1'
        threading.Timer(collect_int, R1_collect).start()
    R1_collect()



main()