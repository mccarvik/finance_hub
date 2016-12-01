
def stringify(strs):
    if isinstance(strs, list):
        return ["'" + str(a) + "'" for a in strs]
    else:
        return "'" + strs + "'"
        

def bootstrap(first_zero_rate, first_mat, bs_rate_mats):
    """
    bs_rate_mats = list of tuples in the format (fwd_rate, maturity)
    """
    new_bs_rate_mats = []
    next_bs_zero_rate = ((bs_rate_mats[0][0] * bs_rate_mats[0][1]) + (first_zero_rate * first_mat)) / (bs_rate_mats[0][1] + first_mat)
    new_bs_rate_mats.append(tuple([bs_rate_mats[0][1] + first_mat, next_bs_zero_rate]))
    for i in range(len(bs_rate_mats)):
        if i == 0:
            continue
        
        next_bs_zero_rate = ((bs_rate_mats[i][0] * bs_rate_mats[i][1]) + \
            (new_bs_rate_mats[-1][1] * new_bs_rate_mats[-1][0])) / \
            (bs_rate_mats[i][1] + new_bs_rate_mats[-1][0])
        new_bs_rate_mats.append(tuple([bs_rate_mats[i][1] + new_bs_rate_mats[-1][0], next_bs_zero_rate]))
    return new_bs_rate_mats
        
    
    
if __name__ == "__main__":
    import pdb; pdb.set_trace()
    print(bootstrap(0.048, 400, [(0.053, 91), (0.055, 98)]))