from reactorpydrive.auth import GoogleAuth
from reactorpydrive.drive import GoogleDrive


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

gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
drive = GoogleDrive(gauth) # Create GoogleDrive instance with authenticated GoogleAuth instance


def get_file_list(directory):
    try:
        file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % directory}).GetList()
        return file_list
    except:
        raise InvalidDir('Specified directory is invalid')


def find_folderid(folder_name, directory):
    file_list = get_file_list(directory)
    no_folders_here = True
    for afile in file_list:
        if afile['mimeType'] == 'application/vnd.google-apps.folder':  # if folder
            no_folders_here = False
            if afile['title'] == folder_name: # Look for folder that matches name
                fid = afile['id']
                return fid
            else:
                raise NotMatching('No folder of that name in specified directory')
    if no_folders_here:
        raise NoFolders('There are no folders in specified directory')


def find_reactorfolder(reactorno):
    r_folder_name = 'R' + str(reactorno)
    wlab_fid = find_folderid('Winkler Lab', 'root')
    rdata_fid = find_folderid('ReactorData', wlab_fid)
    try:
        r_fid = find_folderid(r_folder_name,rdata_fid)
        return r_fid
    except:
        raise NoSuchReactor('There is no reactor with that number')


def find_reactorfile(reactorno, filename):
    tgt_folder_id = find_reactorfolder(reactorno)
    file_list = get_file_list(tgt_folder_id)
    no_file = True
    for afile in file_list:
        if afile['title'] == filename:  # Look for file that matches name
            no_file = False
            fileid = afile
            return fileid
    if no_file:
        return False


def write_to_reactordrive(reactorno, filename, text):
    file_to_write = find_reactorfileid(1, 'test.csv')
    if file_to_write is False:  # Create a new file if file doesn't exist
        tgt_folder_id = find_reactorfolder(reactorno)
        file_to_write = drive.CreateFile({'title': filename, 'mimeType':'text/csv',
            "parents": [{"kind": "drive#fileLink","id": tgt_folder_id}]})
    file_to_write.SetContentString(text)
    file_to_write.Upload()

# Write a dummy file
write_to_reactordrive(1, 'test.csv', 'testing some stuff!')
