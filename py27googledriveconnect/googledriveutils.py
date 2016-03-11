"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Write and read from a google doc


Note: Due to this issue:https://github.com/ctberthiaume/gdcp/issues/11, I had
to run python2.7 in a virtual environment for this to work.  UGH!
"""

import os
import urllib2
import datetime
import time
from xml.etree import ElementTree
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd

"""
Define Custom Errors
"""


class BaseError(Exception):
    """Base error for google drive manipulation and navigation errors."""


class InvalidDir(BaseError):
    """Error for specifying a directory ID that doesn't exist"""


class NotMatching(BaseError):
    """Error for specifying a file name that doesn't exist"""


class NoFolders(BaseError):
    """Error for specifying a directory to find folders in that has no folders
    in it"""


class NoSuchReactor(BaseError):
    """Error for specifying a reactor number to find the directory for"""


"""
Authenticate the connection to google drive
This will open a web browser and prompt for user permission.
"""
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and authenticates
drive = GoogleDrive(gauth)  # Create authenticated GoogleDrive instance


def remove_file(filename):
    """
    Determines if a file exists before trying to delete it
    :param filename: str, name of file to delete
    :return: boolean if the filename doesn't exist
    """
    if os.path.exists(filename):
        os.remove(filename)
    else:
        return False
    return


def get_newdata(reactorno):
    """
    Uses HTTP method to query cRIO server for reactor status
    :param reactorno: int, this is the reactor in question
    :return: list, this is a list of requested values
    """
    # Builds the cRIO web server URL where we will make the GET request
    url = 'http://128.208.236.156:8080/cRIOtoWeb/DataTransfer?reactorno=' + \
          str(reactorno)
    # Makes the GET request
    result = urllib2.urlopen(url).read()
    # Result is a labview "cluster" type variable, (like a struct in java)
    # But it is saved here as an XML string and converted to a parseable form
    root = ElementTree.fromstring(result)
    column_names = [Name.text for Name in root[0][1].findall('Name')]
    column_names.insert(0, 'Date')
    # Returns data and data cleans
    data = [Value.text for Value in root[0][1].findall('Value')]
    ts = time.time()
    ts_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    data.insert(0, ts_date)
    df = pd.DataFrame(columns=column_names)
    df.loc[0] = data
    df = df.set_index('Date')
    return df


def get_file_list(directory):
    """
    Returns a file list given the file ID of a directory folder.
    :param directory: str, this is the file ID of the directory of interest
    :return: file_list, list, this is a list of all the files in the directory
    :exceptions: if the specified ID is invalid, raises an exception.
    """
    # List all files
    try:
        file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" %
                                         directory}).GetList()
        return file_list
    except:
        # If directory id is bad, say so.
        raise InvalidDir('Specified directory is invalid')



def find_folderid(folder_name, directory):
    """
    Returns the id of a folder of a given name in a given directory
    :param folder_name: str, this is the name of folder of interest
    :param directory: str, this is the folder ID of the directory of interest
    :return: str, this is the folder ID from folder_name
    :exception NotMatching: if no folder of specified name is found, raise
    exception
    :exception NoFolders: if there are no folders in the specified directory,
    raise exception
    """
    # get list of files from our directory of interest
    file_list = get_file_list(directory)
    # We'll use this to decide whether we need to raise an error later
    no_folders_here = True
    for afile in file_list:
        # if file is a folder...
        if afile['mimeType'] == 'application/vnd.google-apps.folder':
            no_folders_here = False  # We won't need to raise the error
            if afile['title'] == folder_name:
                # Look for folder that matches name, and save the folder ID
                fid = afile['id']
                return fid
    # If nothing matched, the name was wrong
    if 'fid' in locals() or 'fid' in globals():
        raise NotMatching('No folder of that name in specified dir')
    # if none of files in the list were folders, then say so.
    if no_folders_here:
        raise NoFolders('There are no folders in specified directory')


def find_reactorfolder(reactorno):
    """
    Finds the directory of a specified reactor. (reactors are numbered 1
    thru 6)
    :param reactorno: int, this is the reactor in question
    :return: str, this is the file ID of the specified reactor's directory
    :exception No Such Reactor: if no directory of the specified reactor
    exists, raise an error.
    """
    # folder will be 'R1', 'R2', etc. So make that string.
    r_folder_name = 'R' + str(reactorno)
    # Navigate through the directories
    wlab_fid = find_folderid('Winkler Lab', 'root')
    rdata_fid = find_folderid('ReactorData', wlab_fid)
    try:  # When we find reactordata directory, look for our reactor's folder
        r_fid = find_folderid(r_folder_name, rdata_fid)
        return r_fid
    except:  # If we can't find it, say so.
        raise NoSuchReactor('There is no reactor with that number')


def find_reactorfileid(reactorno, filename):
    """
    Find a specific file withn a specified reactor's directory
    :param reactorno: int, the number of reactor in question
    :param filename: str, the name of file being looked for
    :return: file, this is the file
     OR
    :return: boolean, this is false if there is no file matching specified
    name. The boolean is then used in write_to_reactordrive to make a new file
    """
    # Get file id of our reactor's folder
    tgt_folder_id = find_reactorfolder(reactorno)
    file_list = get_file_list(tgt_folder_id)  # List all files in that folder
    no_file = True
    for afile in file_list:
        if afile['title'] == filename:  # Look for file that matches name
            # Now we know that file exists, so we don't need to make it later
            no_file = False
            fileid = afile
            return fileid  # Return our file of interest
    # If file we asked for doesn't exist, tell next function with a boolean.
    if no_file:
        return False


def write_to_reactordrive(reactorno, filename):
    """
    Writes some specified info to a specified file for a specified reactor
    :param reactorno: int, this is the reactor in question
    :param filename: this is the name of the file we want to write to.
    """
    # Find our file we asked for
    try:
        to_write = get_newdata(reactorno)
        file_to_write = find_reactorfileid(reactorno, filename)
        if file_to_write is False:  # Create a new file if file doesn't exist
            # Find the id of directory we want to save to.
            tgt_folder_id = find_reactorfolder(reactorno)
            # Make that file
            file_to_write = drive.CreateFile({'title': filename,
                                              'mimeType': 'text/csv', "parents":
                                                  [{"kind": "drive#fileLink", "id":
                                                      tgt_folder_id}]})
            # Put the content we want in the file
            to_write.to_csv('temp.csv')
        else:
            file_to_write.GetContentFile('temp.csv')
            old_data = pd.read_csv('temp.csv')
            old_data = old_data.set_index('Date')
            new_data = old_data.append(to_write)
            new_data.to_csv('temp.csv')
        file_to_write.SetContentFile('temp.csv')
        remove_file('temp.csv')

        file_to_write.Upload()  # Upload it
        print 'Collecting Data...'
    except Exception, e:
        ts = time.time()
        ts_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print str(e)
        print 'Due to error, skipped collection at ' + str(ts_date)
    return


def read_from_reactordrive(reactorno, filename, save_file_as):
    """
    Reads a specified file from a specified reactors directory and saves it
    locally.
    :param reactorno: int, this is the reactor in question
    :param filename: this is the name of the file we want to read
    :param save_file_as: str, this is what you want to save the file as.
    :return:
    """
    # find file we asked for
    file_to_read = find_reactorfileid(reactorno, filename)
    if file_to_read is False:
        raise NotMatching('The file specified: '+filename+' does not exist')
    else:
        file_to_read.GetContentFile(save_file_as)

