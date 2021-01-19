import pandas as pd


def seriesToDict(s):
    s_dict = {}
    for index in s.index:
        if pd.isnull(s[index]):
            s_dict[index] = ""
        else:
            s_dict[index] = s[index]
    return s_dict


def dfToDict(df):
    df_dict = {}
    for index, row in df.iterrows():
        df_dict[index] = seriesToDict(row)
    return df_dict