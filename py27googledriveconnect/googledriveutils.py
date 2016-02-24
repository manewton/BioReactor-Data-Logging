"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Write and read from a google doc

To Do:
+Add file reading functions
+Add appending data to existing files functions (write now everything just overwrites)
+Add exporting from cRIO portion


Note: Had to copy of local copy of PyDrive because it has some issues that make it incompatible with the latest
version of the googleAPI.  This copy is in it's own directory and
Specifically, it forces a / at the end of the redirect URI.  Google does not allow a slash at the end of those URLS
so in order to use the package, I had to copy it and remove that / from the end of the procedurally generated URL.
"""

from reactorpydrive.auth import GoogleAuth
from reactorpydrive.drive import GoogleDrive



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
    """Error for specifying a directory to find folders in that has no folders in it"""


class NoSuchReactor(BaseError):
    """Error for specifying a reactor number to find the directory for"""


"""
Autheticate the connection to google drive
This will open a web browser and prompt for user permission.
"""
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
drive = GoogleDrive(gauth) # Create GoogleDrive instance with authenticated GoogleAuth instance


def get_file_list(directory):
    """
    Returns a file list given the file ID of a directory folder.
    :param directory: str, this is the file ID of the directory of interest
    :return: file_list, list, this is a list of all the files in the directory
    :exceptions: if the specified ID is invalid, raises an exception.
    """
    try:
        file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % directory}).GetList()  # List all files
        return file_list
    except:
        raise InvalidDir('Specified directory is invalid')  # If directory id is bad, say so.


def find_folderid(folder_name, directory):
    """
    Returns the id of a folder of a given name in a given directory
    :param folder_name: str, this is the name of folder of interest
    :param directory: str, this is the folder ID of the directory of interest
    :return: str, this is the folder ID from folder_name
    :exception NotMatching: if no folder of specified name is found, raise exception
    :exception NoFolders: if there are no folders in the specified directory, raise exception
    """
    file_list = get_file_list(directory)  # get list of files from our directory of interest
    no_folders_here = True  # We'll use this to decide whether we need to raise an error later
    for afile in file_list:
        if afile['mimeType'] == 'application/vnd.google-apps.folder':  # if file is a folder...
            no_folders_here = False  # We won't need to raise the error
            if afile['title'] == folder_name:
                fid = afile['id'] # Look for folder that matches name, and save the folder ID
                return fid
            else:  # If nothing matched, the name was wrong
                raise NotMatching('No folder of that name in specified directory')
    if no_folders_here:  # if none of files in the list were folders, then say so.
        raise NoFolders('There are no folders in specified directory')


def find_reactorfolder(reactorno):
    """
    Finds the directory of a specified reactor. (reactors are numbered 1 thru 6)
    :param reactorno: int, this is the reactor in question
    :return: str, this is the file ID of the specified reactor's directory
    :exception No Such Reactor: if no directory of the specified reactor exists, raise an error.
    """
    r_folder_name = 'R' + str(reactorno)  # folder will be 'R1', 'R2', etc. So make that string.
    # Navigate through the directories
    wlab_fid = find_folderid('Winkler Lab', 'root')
    rdata_fid = find_folderid('ReactorData', wlab_fid)
    try:  # When we find reactordata directory, look for our reactor's folder
        r_fid = find_folderid(r_folder_name,rdata_fid)
        return r_fid
    except: # If we can't find it, say so.
        raise NoSuchReactor('There is no reactor with that number')


def find_reactorfile(reactorno, filename):
    """
    Find a specific file withn a specified reactor's directory
    :param reactorno: int, the number of reactor in question
    :param filename: str, the name of file being looked for
    :return: file, this is the file
     OR
    :return: boolean, this is false if there is no file matching specified name.
                      The boolean is then used in write_to_reactordrive to make a new file
    """
    tgt_folder_id = find_reactorfolder(reactorno)  # Get file id of our reactor's folder
    file_list = get_file_list(tgt_folder_id) # List all files in that folder
    no_file = True
    for afile in file_list:
        if afile['title'] == filename:  # Look for file that matches name
            no_file = False # Now we know that file exists, so we don't need to make it later
            fileid = afile
            return fileid # Return our file of interest
    if no_file: # If the file we asked for doesn't exist, tell next function with a boolean.
        return False


def write_to_reactordrive(reactorno, filename, text):
    """
    Writes some specified info to a specified file for a specified reactor
    :param reactorno: int, this is the reactor in question
    :param filename: this is the name of the file we want to write to.
    :param text: this is the data we want to write
    """
    file_to_write = find_reactorfileid(1, 'test.csv')  # Find our file we asked for
    if file_to_write is False:  # Create a new file if file doesn't exist
        tgt_folder_id = find_reactorfolder(reactorno)  # Find the id of directory we want to save to.
        file_to_write = drive.CreateFile({'title': filename, 'mimeType':'text/csv',
            "parents": [{"kind": "drive#fileLink","id": tgt_folder_id}]})  # Make that file
    file_to_write.SetContentString(text) # Put the content we want in the file
    file_to_write.Upload()  # Upload it

# Write a dummy file to test
write_to_reactordrive(1, 'test.csv', 'testing some stuff!')
