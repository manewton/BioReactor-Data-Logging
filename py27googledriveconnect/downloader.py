import shutil
import os
from googledriveutils import read_from_reactordrive
from googledriveutils import remove_file

filename = 'R1data.csv'
read_from_reactordrive(1, 'R1data', filename)
curdir = os.path.join(__file__, os.pardir)
pardir = os.path.join(curdir, os.pardir)
move_to = os.path.abspath(pardir)+'/SampleData'
file_to_move = os.path.abspath(curdir)+'/'+filename
if os.path.isfile(move_to+'/'+filename):
    remove_file(move_to+'/'+filename)

shutil.move(file_to_move, move_to)
