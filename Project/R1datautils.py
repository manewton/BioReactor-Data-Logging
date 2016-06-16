"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Read reactor data to google drive every 30 secs.
"""

# Import Libraries
import datetime
import imp
import os
import pandas as pd
from openpyxl import load_workbook
# TODO: Relative imports for bokeh stuff

dl = imp.load_source('downloader', os.getcwd() +
                      '/Project/downloader.py')
gdu = imp.load_source('googledriveutils', os.getcwd() +
                      '/Project/googledriveutils.py')
remove_file = gdu.remove_file
find_folderid = gdu.find_folderid
get_file_list = gdu.get_file_list


# Define constants
COL_LABEL = '\nProbe - '
# TODO: ORP PROBE: REVISE THIS DATE when orp probe is added
IGNORE_BEFORE = pd.to_datetime('5.24.2016')
PROBE_DICT = {'DO (mg/L)': 'DO mg/L',
              'pH': 'pH',
              'NH4+ (mgN/L)': 'Ammonium',
              'ORP (mV)': 'ORP mV'}
TS = '\nTimestamps'


def save_to_workbook(newval,
                     date,
                     header,
                     rows_to_skip=12,
                     wbname='temp.xlsx',
                     sheet_name='Reactor Data'):
    wb = load_workbook(wbname)
    ws = wb.get_sheet_by_name(sheet_name)
    rowno = None
    colno = None
    for col in range(1, ws.max_column):
        # TODO: Error if header isn't found
        if ws.cell(row=rows_to_skip + 1, column=col).value == header:
            colno = col
            break
    for row in range(rows_to_skip+1, ws.max_row):
        # TODO: Error if date isn't found
        if ws.cell(row=row, column=1).value == date:
            rowno = row
            break
    # TODO: Fix this
    ws.cell(row=rowno, column=colno).value = newval
    wb.save(wbname)
    return colno, rowno, ws


def find_r1masterfile():
    # Navigate through the directories
    wlab_fid = find_folderid('Winkler Lab', 'root')
    kp_fid = find_folderid('KathrynsProjects', wlab_fid)
    amxrct_fid = find_folderid('Anammox Reactor', kp_fid)
    trials_fid = find_folderid('Reactor Trials', amxrct_fid)
    # List files in directory
    file_list = get_file_list(trials_fid)
    for afile in file_list:
        if afile['title'] == 'AMX RCT.xlsx':
            # Return the file we asked for
                return afile
        # TODO: error if there was no file with that name


def save_r1masterfile(csv, rows_to_skip=12, filename='temp.xlsx'):
    # Get the file we want
    master_file = find_r1masterfile()
    try:
        master_file.GetContentFile(filename)
    except Exception, e:
        print "Warning: Something wrong with file R1 Master File."
        print str(e)
        # TODO: add an email alarm to responsible user

    if csv:
        return master_file
    else:
        df = pd.read_excel(filename,
                           encoding="utf-16",
                           skiprows=rows_to_skip,
                           sep='\t',
                           index_col='Date',
                           keep_default_na=False,
                           na_values=['-1.#IND', '1.#QNAN', '1.#IND',
                           '-1.#QNAN', '#N/A','N/A', '#NA', 'NA'
                           'NULL', 'NaN', '-NaN', 'nan', '-nan'])
        remove_file(filename)
        # TODO: Is this broken?
        return df


def upload_r1masterfile(filename='temp.xlsx'):
    # Get the file we want
    master_file = find_r1masterfile()
    try:
        master_file.SetContentFile(filename)
        master_file.Upload()
    except Exception, e:
        print "Warning: Something wrong with file R1 Master File."
        print str(e)
        # TODO: add an email alarm to responsible user


def populate_r1masterfile(rows_to_skip=12, filename='temp.xlsx'):
    # Get the R1 master file as a file
    save_r1masterfile(True)
    # Convert the juicy stuff to a dataframe
    masterdf = pd.read_excel(filename,
                             encoding="utf-16",
                             skiprows=rows_to_skip,
                             sep='\t',
                             index_col='Date',
                             keep_default_na=False,
                             na_values=['-1.#IND', '1.#QNAN', '1.#IND',
                             '-1.#QNAN', '','N/A', '#NA', 'NA'
                             'NULL', 'NaN', '-NaN', 'nan', '-nan'])
    # Find what we will populate with probe data
        # Find timestamps
    ts_columns = [col for col in masterdf.columns if TS in col]
    tsdf = masterdf[ts_columns]
        # Find probes, ignore before given date
    probe_columns = [col for col in masterdf.columns if COL_LABEL in col]
    probedf = masterdf[probe_columns]
    probedf = probedf[masterdf.index > IGNORE_BEFORE]
        # Find Indices and column labels of blank values
    stackdf = probedf.stack(dropna=False)
    empty = stackdf[stackdf.isnull()].index.tolist()

    # For each blank look for the probe, time & date of cycle, and return val
    for each in empty:
        probe, time = each[1].split(COL_LABEL)
        time = tsdf.loc[each[0], time+TS]
        ts = each[0]+pd.DateOffset(hour=time.hour, minute=time.minute)
        val = dl.get_val_from(1, ts, PROBE_DICT.get(probe))
        probedf.set_value(each[0], each[1], val)
        #Save that value to the workbook
        save_to_workbook(val, each[0], each[1])
    upload_r1masterfile()
    print 'Master file updated. ' + str(datetime.datetime.now())
    remove_file('temp.xlsx')
    return probedf
