from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Creates local webserver and auto handles authentication
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

"""
Function GetGDriveContent
Input:
    drive - GoogleDrive to be accessed
Output:
    list_of_content - list of files and folders in the GoogleDrive root (list)
"""
def GetGDriveContent(drive):
    # The line below auto-iterates through all files that matches this query
    file_list = drive.ListFile({'q':
        "'root' in parents and trashed=false"}).GetList()
    list_of_content = []
    for file1 in file_list:
        list_of_content.append(file1['title'])
    return list_of_content


"""
Function CreateFileOnGDrive creates a file with name 'filename'
in GDrive root directory
Input:
    drive - GoogleDrive to be accessed
    filename - name of the file to be created (string)
    content - content to be inserted in the file (string)
Output:
    None
"""
def CreateFileInGDriveRoot(drive,filename,content):
    GDriveContent = GetGDriveContent(drive)
    if filename in GDriveContent:
        print 'A file with name', filename, 'arleady exists in GDrive'
    else:
        file1 = drive.CreateFile({'title': filename})
        file1.SetContentString(content)
        file1.Upload()


def GetFolderID(drive,foldername):
    file_list = drive.ListFile({'q':
        "'root' in parents and trashed=false"}).GetList()
    for item in file_list:
        if item['title'] == foldername:
            folder_id = item['id']
    return folder_id


def CreateFolderInGDriveRoot(drive,foldername):
    GDriveContent = GetGDriveContent(drive)
    if foldername in GDriveContent:
        print 'A folder with name', foldername, 'arleady exists in GDrive'
    else:
        file1 = drive.CreateFile({'title': foldername,
            'mimeType' : 'application/vnd.google-apps.folder'})
        file1.Upload()


"""
Function CreateFileInGDriveFolder is still under construction
"""
def CreateFileInGDriveFolder(drive,folder,filename,content):
        file1 = drive.CreateFile({'title': filename})
        file1.SetContentString(content)
        file1.Upload()

#Line below creates a folder CSE599TestFolder in my GDrive
CreateFolderInGDriveRoot(drive,'CSE599TestFolder')

#print 'exam1 folder id is', GetFolderID(drive,'exam1')

#CreateFileInGDriveRoot(drive,'Hello3.txt','Hello world!')
#print GetGDriveContent(drive)
