# BioReactor-Data-Logging
Live and Remote Streaming of key Sequencing Batch Reactor data in a web interface.

### Directory Structure
Herein the package will have three main sub-directories: Tests, Projects, For 
Future, and Data_management.
- The Projects directory will contain the 2.7 code and unit tests for all functioning tools to date.
- The For Future directory contains example code that might be handy in the future.
- The Data_Management directory contains all 3.5 code required to data clean reactor data.


### How does it work?
- Data is pulled from a reactor in the Winkler lab using urllib2 as an XML 
string and parsed into a dataframe using elementtree and pandas.(Function: 
in googledriveutils.py, get_newdata())
- That data is then appended to the data already in the google drive using 
PyDrive. (Function: in googledriveutils.py, write_to_reactordrive())
- The full dataframe can then be downloaded to be manipulated as needed. 
(Function: in downloader.py, download_latest())
- This work flow is done every 30 seconds. (Script: in scheduler.py)
- The full dataframe is then streamed onto a bokeh server and plotted against 
time. (Script: in bokehplot.py)


### How can I use it?
This cannot be done from an ipython notebook since the final project requires
running a local server on your computer.  To view live streaming data you will
need:
1) A mac computer (write_to_reactordrive() function doesn't work from a pc right
now.)
2) Python 2.7
3) These Pacakges: urllib2, XML Element tree, os, datetime, time, pandas

Once you have all that, do the following.
1) In Terminal cd to the bioreactor repo.
2) In Terminal run _python scheduler.py_
3) In a separate terminal screen (or on a pc if you prefer) run _bokeh serve_
4) On the same computer as the computer running the bokeh server, open a new 
terminal screen.
5) run _python bokehplot.py_

__Ta-Da!__


### License
This package is covered by GPL (V3) which requires anyone who distributes this 
code or a derivative work to make the source available under the same terms. 
This license was chosen in order to more easily and freely affect future 
improvements upon the developed functionality herein.