import pandas as pd
def merge_datafram_function:
    sample = pd.read_csv("sampledatalive.csv")
    test = pd.read_csv("test 1-31-16.csv", encoding = "utf-16", skiprows=9, sep = '\t')
    return sample.join(test)


"""
Adding some comments to experiment with git and pull_requests

"""
