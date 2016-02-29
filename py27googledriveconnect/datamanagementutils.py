"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Write and read from a google doc

To Do:
+Add appending data to existing files functions (now everything just overwrites)
+Add exporting from cRIO portion
"""

import easywebdav

webdav = easywebdav.connect(
    host='128.208.236.156/files',
    username='_googledrive_',
    port=443,
    protocol="https",
    password='_access_',
    verify=False
    )

_file = "test.py"

print webdav.cd("/C/")
print webdav._get_url("")
print webdav.ls()
print webdav.exists("/dav/test.py")
print webdav.exists("ECS.zip")
print webdav.download(_file, "./"+_file)
print webdav.upload("./test.py", "test.py")

import csv
import pandas as pd
from googledriveutils import read_from_reactordrive, write_to_reactordrive, remove_file


def add_new_data(reactorno, file_to_read, file_to_write):
    read_from_reactordrive(reactorno, file_to_read, 'tempdata.csv')


def get_local_data(x):
    """
    Get the local data from the cRIO and save in a temp file.
    :param x: int, dummyvar
    :return y: str, returns something to write.
    """



