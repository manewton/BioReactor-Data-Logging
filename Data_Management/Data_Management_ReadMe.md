# Data_Management Directory 

The purpose of this directory: 

  - Host directory for downloading bioreactor data from google drive: R1Data
  - Contains Data_Management.py functions for data merging
  -         add_and_merge_inst2_data(filename):
  -         instrument3_input_v2():
  - Will serve as place to upload spectrophotometer data (instrument_2) 

### Worlflow 
1)  Import present data from google drive:
    
    This is done by running downloader.py (in the Project directory). 
    
    
    Note that this is a python 2.7 code. Using a virtual environment is recommended. downloader.py will download R1Data from google drive (this is the live streaming data from the bioreactor), into Data_Management direcotry. 
    
2) Clean and join manually imported data using the following function:

        add_and_merge_inst2_data(filename)
        
    This function is in Data_Management.py file and it uses python 3.5. This cleans up the .csv that is manually imported via a USB stick. It then merges the cleaned up data frame with the R1Data file that was downloaded in step 1 and saves it as R1Data. This file is ready to be sent back to google drive now that it contains the spectrophotomer data. 

3) Manually enter data and join with R1Data using:

        instrument3_input_v2()

    Function is part of Data_Management.py file. It takes R1Data file and asks for user to input additional data column with a timestamp. It then joins this data column to the R1Data and saves it as a newer version of R1Data. This file is ready to be sent back to google drive. 
 
4) Send the modified and merged file back to google drive using the following function: 

        writeelse_to_reactordrive(reactorno, filename, InputFile):
    
    This function is a python 2.7 function so recommended to use virtual environment. This function is in the Project directory and in the googledriveutils.py file. 



