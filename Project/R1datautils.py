"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Read reactor data to google drive every 30 secs.

To Do:

"""

import pandas as pd
import numpy as np
from operator import methodcaller
from googledriveutils import find_folderid, get_file_list, remove_file
import downloader as dl
import datetime
 # coding: utf-8


def find_r1masterfile(csv, rows_to_skip=12, filename='temp.csv'):
    # Navigate through the directories
    wlab_fid = find_folderid('Winkler Lab', 'root')
    kp_fid = find_folderid('KathrynsProjects', wlab_fid)
    amxrct_fid = find_folderid('Anammox Reactor', kp_fid)
    trials_fid = find_folderid('Reactor Trials', amxrct_fid)
    # List files in directory
    file_list = get_file_list(trials_fid)
    for afile in file_list:
        if afile['title'] == 'AMX RCT.xlsx':
            # Get the file we want
            try:
                afile.GetContentFile(filename)
            except Exception, e:
                print "Warning: Something wrong with file R1 Master File."
                print str(e)
                #TODO: add an email alarm to responsible user

            if csv:
                return afile
            else:
                df = pd.read_excel(filename,
                                   encoding="utf-16",
                                   skiprows=rows_to_skip,
                                   sep='\t')
                remove_file(filename)
                # This is broken
                return df


def populate_r1MasterFile(rows_to_skip=12, filename='temp.csv'):
    # Get the R1 master file as a file
    find_r1masterfile(True, filename=filename)
    # Convert the juicy stuff to a dataframe
    masterdf = pd.read_excel(filename,
                             encoding="utf-16",
                             skiprows=rows_to_skip,
                             sep='\t',)
    # Find all of the columns that we will auto populate with probe data
    probe_columns = [col for col in masterdf.columns if '\nProbe' in col]

    # Look for blanks in those columns
    for col in probe_columns:
        # If we find a blank value, get the three time stamps for that trial
        yyyymmdd = masterdf.loc[np.isnan(masterdf[col]), 'Date']
        t_begin = masterdf.loc[np.isnan(masterdf[col]), 'Begin\nTimestamps']
        #t_begin = yyyymmdd.map(pd.Timestamp.date)  +  t_begin.map(pd.Timestamp)
        print type(t_begin) #TODO: Convert this to a timestamp and then add to date
        #dataframe["period"] = dataframe["Year"].map(str) + dataframe["quarter"]
        #TODO: find a way to concatenate these two columns as one string.
        #t_end_anaerobic = yyyymmdd + masterdf.loc[
        #    np.isnan(masterdf[col]), 'End of Anaerobic\nTimestamps']
        #t_end_aerobic = yyyymmdd + masterdf.loc[
        #    np.isnan(masterdf[col]), 'End of Aerobic\nTimestamps']
        # Convert those to datetime objects
        ts_begin = datetime.datetime.strptime('%Y-%m-%d %H:%M', t_begin)
        ts_end_anaerobic = datetime.datetime.strptime('%Y-%m-%d %H:%M',
                                                      t_end_anaerobic)
        ts_end_aerobic = datetime.datetime.strptime('%Y-%m-%d %H:%M',
                                                    t_end_aerobic)



    return masterdf
    #ts_begin
    #ts_end_anaerobic
    #ts_end_aerobic



masterdf=populate_r1MasterFile()