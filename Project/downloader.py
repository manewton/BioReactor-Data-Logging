"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Downloads most recent copy of reactor data.
"""

import os
from googledriveutils import read_from_reactordrive
from googledriveutils import remove_file


def download_latest(reactorno=1, filename='R1data'):
    """
    Downloads most recent copy of specified reactor data given specifed file.
    :param reactorno: int, number of reactor to download data for
    :param filename: str, name of tile to download from google drive.
    :return:
    """
    curdir = os.getcwd()
    pardir = os.path.abspath(os.path.join(curdir, os.pardir))
    save_to = pardir+'/Data_Management/'+filename
    if os.path.isfile(save_to):
        remove_file(save_to)
    read_from_reactordrive(reactorno, filename, save_to)
    return

download_latest()
