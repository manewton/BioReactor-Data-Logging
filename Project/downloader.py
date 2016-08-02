"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Downloads most recent copy of reactor data.
"""

import pandas as pd
import datetime
from googledriveutils import list_rfiles_by_date, read_from_reactordrive

# TODO: Make more efficient

# Constants
TEN_MINS = datetime.timedelta(minutes=10)


class BaseError(Exception):
    """Base error for google drive manipulation and navigation errors."""


class InvalidParam(BaseError):
    """Specified parameter is invalid."""


class NotAvailable(BaseError):
    """No data available at that time."""


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
    # If we want a range of entries, find the earliest timestamp
    # TODO: error if date is before now or out of collection range
    if timestamp2 is False:
        df = read_from_reactordrive(reactorno, timestamp.date())
        df['Absolute Time Diff'] = abs(df.index - timestamp)
        # If no data is available for that point, say so
        if df['Absolute Time Diff'].min() < TEN_MINS:
            tgt_idx = df['Absolute Time Diff'].argmin()
            our_vals = df.loc[tgt_idx]
            our_vals = our_vals.drop('Absolute Time Diff')
        else:
            raise NotAvailable('at time: ' + timestamp)
    else:
        ts_formatted2 = pd.to_datetime(timestamp2)
        if ts_formatted < ts_formatted2:
            ts_first = ts_formatted
            ts_second = ts_formatted2
        else:
            ts_first = ts_formatted2
            ts_second = ts_formatted
        delta_t = ts_second-ts_first
        if delta_t.days > 1:
            # do something else
            # TODO complete this...
            latest_file, file_idents = list_rfiles_by_date(reactorno)
            for each in file_idents:
                if each[2] > ts_first.date() and each[2] < ts_second.date():
                    df = read_from_reactordrive(reactorno, ts_first)
        else:
            df = read_from_reactordrive(reactorno, ts_first)
        df['Absolute Time Diff'] = abs(df.index-ts_first)
        df['Absolute Time Diff2'] = abs(df.index - ts_second)
        # If no data is available for that point, say so
        if df['Absolute Time Diff'].min() > TEN_MINS:
            raise NotAvailable('at time: ' + str(timestamp))
        elif df['Absolute Time Diff2'].min() > TEN_MINS:
            raise NotAvailable('at time: ' + str(timestamp2))
        else:
            tgt_idx = df['Absolute Time Diff'].argmin()
            tgt_idx2 = df['Absolute Time Diff2'].argmin()
            our_vals = df.loc[tgt_idx:tgt_idx2]
            our_vals.drop(['Absolute Time Diff', 'Absolute Time Diff2'],
                          axis=1)
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
        raise InvalidParam('Specified parameter ' + str(val) + ' is invalid')


