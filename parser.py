import pandas as pd


def seriesToDict(s):
    s_dict = {}
    for index in s.index:
        if pd.isnull(s[index]):
            s_dict[index] = ""
        else:
            s_dict[index] = s[index]
    return s_dict