"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Downloads most recent copy of reactor data.
"""

import datetime
from googledriveutils import list_rfiles_by_date, read_from_reactordrive
import pandas as pd


class BaseError(Exception):
    """Base error for google drive manipulation and navigation errors."""


class InvalidParam(BaseError):
    """Specified parameter is invalid."""


def get_values_from(reactorno, timestamp, timestamp2=False):
    """
    Gets values from the reactor from a given timestamp or time range
    :param reactorno: Number of reactor we are querying
    :param timestamp: Timestamp of data point we're interested in.
    :param timestamp2: Optional, for a time range of points, specify 2nd pt
    :return:
    """
    # Format our timestamp properly
    ts_formatted = pd.to_datetime(timestamp)
    # Get the reactor files
    latest_file, file_idents = list_rfiles_by_date(reactorno)
    latest_ts = file_idents[3]
    # If we want a range of entries, find the earliest timestamp
    if timestamp2 == False:
        ts_first = timestamp
    else:
        ts_formatted2 = pd.to_datetime(timestamp2)
        if ts_formatted < ts_formatted2:
            ts_first = ts_formatted
            ts_second = ts_formatted2
        else:
            ts_first = ts_formatted2
            ts_second = ts_formatted
    # Check to see if we have to download all the files or just the latest
    if ts_first >= latest_ts:
        df = read_from_reactordrive(reactorno, True)
    else:
        df = read_from_reactordrive(reactorno, False)
    # Find the time point closest to our first/only timestamp
    df['Absolute Time Diff'] = abs(df.index - ts_first)
    tgt_idx = df['Absolute Time Diff'].argmin()
    if timestamp2 == False:
        # Return the one point entry if that's all we wanted
        our_vals = df.loc[tgt_idx]
        our_vals = our_vals.drop('Absolute Time Diff')
    else:
    # For a range, find the point closest to our 2nd timestamp
        df['Absolute Time Diff2'] = abs(df.index - ts_second)
        tgt_idx2 = df['Absolute Time Diff2'].argmin()
        # Return the range if that's what we asked for
        our_vals = df.loc[tgt_idx:tgt_idx2]
        del our_vals['Absolute Time Diff']
        del our_vals['Absolute Time Diff2']
    return our_vals


def get_val_from(reactorno, timestamp, val, timestamp2=False):
    """
    Returns a specific value at a specific time or range of times.
    :param reactorno: Number of reactor we are querying
    :param timestamp: Timestamp of data point we're interested in.
    :param val: The label of the column we want
    :param timestamp2: Optional, for a time range of points, specify 2nd pt
    :return:
    """
    if timestamp2 == False:
        # For one point, just get one point df
        our_vals = get_values_from(reactorno, timestamp)
    else:
        # Get range df if that's what we wanted
        our_vals = get_values_from(reactorno, timestamp, timestamp2)
    try:
        # Try the user supplied column label
        our_val = our_vals[val]
        return our_val
    except:
        # If that doesn't work, tell user they used a bum label.
        raise InvalidParam('Specified parameter ' + val + ' is invalid')


