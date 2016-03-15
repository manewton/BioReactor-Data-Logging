import pandas as pd
import datetime


def add_and_merge_inst2_data(filename):
    """
    Takes R1Data file and merges another filename into it by time index.
    Returns .csv file titles R1Data with additional columns of data all indexed by time.
    """
    #R1 - first data file parse by data
    R1 = pd.read_csv("R1Data")
    R1date = pd.DatetimeIndex(R1["Date"])
    R1_indexed = R1.set_index(R1date)

    #R2 - second data file (input) is parsed by date
    R2 = pd.read_csv(filename, encoding = "utf-16", skiprows=8, sep = '\t')
    R2 = R2.ix[1:]
    R2 = R2[R2["Sample/ctrl ID"].str.contains("R1")]
    R2date = pd.DatetimeIndex(R2["Result time"])
    R2_indexed = R2.set_index(R2date)
    joined_data = R1_indexed.join(R2_indexed, how = "outer", rsuffix = "_y")
    #I now learned that the rsuffix will append an _y to any repeating columns
    #and there will be repeating columns when we try to add more and more data
    #The correct fucntion would be to us append. which will simple append new data
    #to the existing columns. But only had experimental file of each type so missed
    #this error. Will try to fix once we succesful push this to google drive
    #and effectively add, newly needed columns.

    return joined_data.to_csv("R1Data", sep = ",", index_label=False)



def instrument3_input_v2():
    """
    Takes R1Data and adds a new column with a user input function. return csv
    titled R1Data. Can then be used to push it to google drive.
    """

    #importing present R1Data file
    R1 = pd.read_csv("R1Data")
    R1date = pd.DatetimeIndex(R1["Date"])
    R1_indexed = R1.set_index(R1date)

    #creating dataframe for manually entered data
    inst3_input = input("enter result from instrument 3: ")
    time = datetime.datetime.now()
    R3 = pd.DataFrame([[float(inst3_input),time]], columns = ['Inst_3_Value',"Date"])

    #indexing created datafram by date
    inst3_time = pd.DatetimeIndex(R3["Date"])
    R3_indexed = R3.set_index(inst3_time)

    #joning the data frames by index
    joined_data = R1_indexed.join(R3_indexed, how = "outer", rsuffix = "_y")
    joined_data.to_csv("R1Data", sep = ",", index_label="Date")

    return joined_data.to_csv("R1Data", sep = ",", index_label="Date")




def instrument3_input():
    """
    Updates existing .csv file titled instrument_3 with a user input and
    overwrites the file with the added value. Designed to create a .csv file
    with manually input parameters from instrument #3.
    """

    inst3_df = pd.read_csv("instrument_3")
    inst3_input = input("enter result from instrument 3: ")
    time = datetime.datetime.now()
    df2 = pd.DataFrame([[float(inst3_input),time]], columns = ['Value',"Date"])
    inst3_df = inst3_df.append(df2, ignore_index=True)
    inst3_df.to_csv("instrument_3", sep = ",", index_label=False)
    return inst3_df
