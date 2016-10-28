import datetime

class FixedRateBond():
    """This class will hold all the variables associated with a fixed rate bond"""
    
    def __init__(self, mat_dt, issue_dt):
        self.mat_dt = mat_dt
        self.issue_dt = issue_dt