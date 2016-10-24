
def stringify(strs):
    if isinstance(strs, list):
        return ["'" + a + "'" for a in strs]
    else:
        return "'" + strs + "'"