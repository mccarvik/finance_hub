

def update_check(list1, list2):
    for i,j in zip(list1, list2):
        if i != j:
            return True
    return False