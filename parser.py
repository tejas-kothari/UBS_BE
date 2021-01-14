def seriesToDict(s):
    s_dict = {}
    for index in s.index:
        s_dict[index] = s[index]
    return s_dict