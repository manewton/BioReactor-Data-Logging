"""
Written By: Kathryn Cogert
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Write and read from a google doc

To Do:
+Add appending data to existing files functions (now everything just overwrites)
+ Add unit tests
+ add errors
"""
import urllib2
import datetime
import time
import os
from xml.etree import ElementTree
import pandas as pd
from googledriveutils import read_from_reactordrive
from googledriveutils import write_to_reactordrive


def get_newdata(reactorno):
    """
    Uses HTTP method to query cRIO server for reactor status
    :param reactorno: int, this is the reactor in question
    :param info: str, defines what you want from the data
                    ='data' is the values
                    ='columns' is the names of the columns
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
    data=[Value.text for Value in root[0][1].findall('Value')]
    ts= time.time()
    ts_date=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    data.insert(0,ts_date)
    df = pd.DataFrame(columns=column_names)
    df.loc[0]=data
    return df

def create_new_file(reactorno, filename):
    """
    Creates a new file locally with columns defined by reactor status XML file
    :param reactorno: int, this is the reactor in question
    :param filename: str, this is the name of the file we want to create
    :return:
    """
    # Get reactor status
    new_data = get_newdata(reactorno)
    # Define new empty dataframe with column names from XML
    # Save as a CSV
    new_data.to_csv(filename)
    return new_data  # Return the new df in case you need it

def append_data(reactorno, filename):
    # Download latest data into a dataframe
    new_data = get_newdata(reactorno)
    read_from_reactordrive(reactorno, filename, filename)
    # Check to make sure data is still formatted the same
    old_data = pd.read_csv(filename)
    to_write = old_data.append(new_data)
    write_to_reactordrive(reactorno, filename, to_write)
    remove_file(filename)
    return to_write


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
