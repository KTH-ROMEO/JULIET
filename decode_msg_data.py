SID_TO_N1 = {
    0xAAAA: 3,  
    0x5555: 2,  
}

class HK_uC_Report:
    def __init__(self):
        self.vbat_i             = 0
        self.temperature_i      = 0
        self.uc3v_i             = 0

class HK_FPGA_Report:
    def __init__(self):
        self.fpga3v_i           = 0
        self.fpga1p5v_i         = 0


def decode_HK_data():
    pass