
import os
from googledriveutils import read_from_reactordrive
from googledriveutils import remove_file

def download_latest(reactorno=1, filename='R1data',):
    curdir = os.getcwd()
    pardir = os.path.abspath(os.path.join(curdir, os.pardir))
    save_to = pardir+'/DataManagement/'+filename
    if os.path.isfile(save_to):
        remove_file(save_to)
    read_from_reactordrive(reactorno, filename, save_to)
    return

download_latest()