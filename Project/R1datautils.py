"""
Written By: Kathryn Cogert
For: Winkler Lab Bioreactor DataLogging
May, 2016
Purpose: Allow access and manipulation of the master reactor 1 data file.
"""

# Import Libraries
import datetime
import imp
import os
import pandas as pd
from openpyxl import load_workbook

# Can't import local modules absolutely with bokeh, so doing it relatively
dl = imp.load_source('downloader', os.getcwd()+'/Project/downloader.py')
gdu = imp.load_source('googledriveutils', os.getcwd() +
                      '/Project/googledriveutils.py')
find_folderid = gdu.find_folderid
get_file_list = gdu.get_file_list
remove_file = gdu.remove_file

# Define constants
COL_LABEL = '\nProbe - '
# TODO: ORP PROBE: REVISE THIS DATE when orp probe is added
IGNORE_BEFORE = pd.to_datetime('6.1.2016')
PROBE_DICT = {'DO (mg/L)': 'DO mg/L',
              'ORP (mV)': 'ORP mV',
              'pH': 'pH',
              'NH4+ (mgN/L)': 'NH4 mg/L'}
TS = '\nTimestamps'


def save_to_workbook(newval,
                     date,
                     header,
                     rows_to_skip=12,
                     wbname='temp.xlsx',
                     sheet_name='Reactor Data'):
    """
    Saves a given value into a given workbook at a given location
    :param newval: string, int, float, etc., the value to save
    :param date: datetime object, the date (aka row in master file) to look for
    :param header: string, the column name to look for.
    :param rows_to_skip: int, the rows to skip before column headers start
    :param wbname: string, the name of the workbook
    :param sheet_name: string, the name of the sheet
    :return: tuple, row number, column number, value written
    """
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
    """
    Look for the R1 master file in google drive.
    :return: googledriveobject, the file we want
    """
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
    """
    Save the R1 master file from google drive as local file or dataframe.
    :param csv: boolean, if true, save as file, else return a dataframe
    :param rows_to_skip: int, number of rows to skip (if returning dataframe)
    :param filename: string, file to save as (if returning the file)
    :return:
    """
    # Get the file we want
    master_file = find_r1masterfile()
    # Try downloading the file and return an error if that doesn't work
    try:
        # This mimetype allows downloading google sheets file as a .xlsx
        master_file.GetContentFile(filename,
                                   mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception, e:
        print "Warning: Something wrong with downloading R1 Master File save."
        print str(e)
        return e
        # TODO: add an email alarm to responsible user
    if csv: # If we want as a csv...
        return master_file
    else: # If we want as a dataframe...
        df = pd.read_excel(filename,
                           skiprows=rows_to_skip,
                           sep='\t',
                           index_col='Date')
        remove_file(filename)
        # TODO: Is this broken?
        return df


def upload_r1masterfile(filename='temp.xlsx'):
    """
    Upload a given file to drive as our master file
    :param filename: name of local file to upload
    :return:
    """
    # Get the file we want from drive
    master_file = find_r1masterfile()
    # Try uploading the file and if it doesn't work return an error
    try:
        master_file.SetContentFile(filename)
        # Convert parameter will convert the .xlsx file to a google sheets file
        master_file.Upload(param={'convert': True})
        print 'Master file updated. ' + str(datetime.datetime.now())
        return
    except Exception, e:
        print "Warning: Something wrong with uploading R1 Master File."
        print str(e)
        return e
        # TODO: add an email alarm to responsible user


def populate_r1masterfile(rows_to_skip=12, filename='temp.xlsx'):
    """
    Populate the R1 masterfile with values of interest & upload back to drive.
    :param rows_to_skip:  int, number of rows to skip before dataframe starts
    :param filename: name of file to get data from (local version)
    :return: master file as dataframe.
    """
    # Get the R1 master file as a file
    e = save_r1masterfile(True)
    if e:
        return
    # Convert the juicy stuff to a dataframe
    masterdf = pd.read_excel(filename,
                             skiprows=rows_to_skip,
                             sep='\t',
                             index_col='Date')
    # Find all of the columns that we will auto populate with probe data
    probe_columns = [col for col in masterdf.columns if COL_LABEL in col]
    ts_columns = [col for col in masterdf.columns if TS in col]
    tsdf = masterdf[ts_columns]
    # Make sure we're including the date
    # Define the probe df and ignore everything before constant, given date
    probedf = masterdf[probe_columns]
    probedf = probedf[masterdf.index > IGNORE_BEFORE]
    # Ignore everything before the ORP probe was added
    # Find all the blanks in the columns we can auto populate
    for col in probedf.columns:
        blankdf = probedf[pd.isnull(probedf[col])]
        # If there are empties then fill them.
        if ~blankdf.empty:
            probe, point = col.split(COL_LABEL)
            # TODO: Make this more efficient
            for each in blankdf.index:
                # Get the timestamps of the empties
                time = tsdf.loc[each, point+TS]
                ts = each + pd.DateOffset(hour=time.hour,
                                          minute=time.minute)
                # Get the relevant value
                val = dl.get_val_from(1, ts, PROBE_DICT.get(probe))
                # Assign to the dataframe
                print each, col, val
                probedf.set_value(each, col, val)
                save_to_workbook(val, each, col)
    e = upload_r1masterfile()
    if e:
        return
    return probedf

populate_r1masterfile()
