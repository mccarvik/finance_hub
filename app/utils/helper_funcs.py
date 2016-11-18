
def stringify(strs):
    if isinstance(strs, list):
        return ["'" + str(a) + "'" for a in strs]
    else:
        return "'" + strs + "'"