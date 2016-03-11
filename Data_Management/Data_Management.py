import pandas as pd
import datetime



def merge_dataframe():
    """
    This function takes two specific .csv file titles in the present working

    """
    instrument_1 = pd.read_csv("sampledatalive.csv")
    instrument_2 = pd.read_csv("test 1-31-16.csv", encoding = "utf-16", skiprows=9, sep = '\t')
    return instrument_1.join(instrument_2)


def instrument2_cleanup():
    """
    Takes file csv file from instrument 2 and cleans it up. spits out a .csv
    file titled instrument_3.
    """
    instrument_2 = pd.read_csv("test 1-31-16.csv", encoding = "utf-16", skiprows=8, sep = '\t')
    instrument_2 = instrument_2.ix[1:]
    instrument_2 = instrument_2[instrument_2["Sample/ctrl ID"].str.contains("R1")]
    instrument_2.to_csv("instrument_3", sep = ",", index_label=False)
    return instrument_2



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




<<<<<<< HEAD


"""
Adding some comments to experiment with git and pull_requests

"""
=======
>>>>>>> master
