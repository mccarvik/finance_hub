

class IR_Swap():
    """ Class to represent a fixed for floating swap """
    
    def __init__(self, tenor=5, fixed_rate=0.04, fixed_pay_freq=0.5,
                float_pay_freq=0.5, float_pay_reset=0.5, float_ref='6M libor'):
        self._tenor = tenor
        self._fixed_rate = fixed_rate
        self._fixed_pay_freq = fixed_pay_freq
        self._float_pay_freq = float_pay_freq
        self._float_pay_reset = float_pay_reset
        self._float_ref = float_ref