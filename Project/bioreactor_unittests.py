import unittest
import os
import pandas as pd
import numpy as np
import sys
import types
from downloader import download_latest
from googledriveutils import remove_file, find_reactorfolder
from googledriveutils import find_reactorfileid, get_newdata, get_file_list

dates = pd.date_range('20130101', periods=6)
data = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))

class TestBioreactor(unittest.TestCase):


    def test_download_latest(self):
        '''
        Test the download_latest function. It should return true
        '''
        download_result = download_latest()
        assert download_result is None


    def test_remove_file(self):
        '''
        Test the remove_file function when the file doesn't exist.
        '''
        #os.remove('nonexistent_file')
        remove_result = remove_file('nonexistent_file')
        self.assertFalse(remove_result)


    def test_find_reactorfolder(self):
        '''
        Test the find_rectorfolder function. That function return reactor id,
        if the result is successful. The id of reactor #1 is
        '0B4idCyQOSLaBVi1rTFZhTkUzSk0'. Testing successful result.
        '''
        reactorfolder_result = find_reactorfolder(1)
        self.assertEqual(reactorfolder_result, '0B4idCyQOSLaBVi1rTFZhTkUzSk0')


    def test_find_reactorfolder_none(self):
        '''
        Test the find_rectorfolder function. That function return reactor id,
        if the result is successful, and returns None if the results is
        unsuccessful. Testing unsuccessful result.
        '''
        reactorfolder_result = find_reactorfolder(999)
        self.assertIsNone(reactorfolder_result)


    def test_find_reactorfileid(self):
        '''
        Test the find_rectorfile function. That function return the id of
        a specific file within a specified reactor's directory
        if the result is successful, and returns False if unsuccessful.
        Testing successful result using R1data file which exist within
        the directory of the reactor #1.
        '''
        reactorfileid_result = find_reactorfileid(1, 'R1data')['title']
        self.assertEqual(reactorfileid_result, 'R1data')


    def test_find_reactorfileid_none(self):
        '''
        Test the find_rectorfile function. That function return the id of
        a specific file within a specified reactor's directory
        if the result is successful, and returns False if unsuccessful.
        Testing unsuccessful result using R999data file which doesn't exist
        within the directory of the reactor #1.
        '''
        reactorfileid_result = find_reactorfileid(1, 'R999data')
        self.assertFalse(reactorfileid_result)


    def test_get_newdata(self):
        '''
        Test the get_newdata function. The funtion returns a Pandas dataframe
        with bioreactor data. Test that the first column name is 'Media Pump',
        which is a real column in the Reactor #1 data frame.
        '''
        get_newdata_result = get_newdata(1)
        self.assertEqual(get_newdata_result.columns[0], 'Media Pump')


    def test_get_newdata_none(self):
        '''
        Test the get_newdata function. The funtion returns a Pandas dataframe
        with bioreactor data. Test that the function returns an empty data
        frame for which we need to call the function using nonexistent
        reactor number (999 for example). The length of the empty data frame
        is 1.
        '''
        get_newdata_result = get_newdata(999)
        self.assertEqual(len(get_newdata_result), 1)


    def test_get_file_list(self):
        '''
        Test the get_file_list function. The funtion returns a list with a
        content of GDrive. We check if its type is 'list'.
        '''
        get_file_list_result = get_file_list('0B4idCyQOSLaBVi1rTFZhTkUzSk0')
        self.assertTrue(isinstance(get_file_list_result, list))


if __name__ == '__main__':
    unittest.main()
