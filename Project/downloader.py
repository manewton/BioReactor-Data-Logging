"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Downloads most recent copy of reactor data.
"""

import os
import datetime
from googledriveutils import read_from_reactordrive
from googledriveutils import remove_file

read_from_reactordrive(1, 'testing.csv', 0)
