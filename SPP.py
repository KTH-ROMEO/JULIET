class SPP_header:
    def __init__(self):
        self.spp_version = 0
        self.packet_type = 0
        self.sec_head_flag = 0
        self.apid = 0
        self.seq_flags = 0
        self.sc = 0
        self.data_len = 0
    
    def __str__(self) -> str:
        f_list = [self.spp_version, self.packet_type, self.sec_head_flag, self.apid, self.seq_flags, self.sc, self.data_len]
        n_list = ["spp_version", "packet_type", "sec_head_flag" , "apid", "seq_flags", "sc", "data_len"]
        s_list = []
        for i, f in enumerate(f_list):
            s_list.append(n_list[i] + ": " + str(f))
        res = '\n'.join(s_list)
        res += '\n'
        return res
    
    def simple_TC(self, shf, apid, dl):
        self.packet_type = 1
        self.sec_head_flag = shf
        self.apid = apid
        self.data_len = dl
    
    def SPP_encode(self):
        result_buffer = [0] * 6
        
        result_buffer[0] |=  self.spp_version << 5
        result_buffer[0] |=  self.packet_type << 4
        result_buffer[0] |=  self.sec_head_flag << 3
        result_buffer[0] |= (self.apid & 0x300) >> 8
        result_buffer[1] |=  self.apid & 0x0FF
        result_buffer[2] |=  self.seq_flags << 6
        result_buffer[2] |= (self.sc  & 0x3F00) >> 8
        result_buffer[3] |=  self.sc  & 0x00FF
        result_buffer[4] |= (self.data_len & 0xFF00) >> 8
        result_buffer[5] |=  self.data_len & 0x00FF
        return bytearray(result_buffer)
    
    
def SPP_decode(raw_header):
    primary_header = SPP_header()
    primary_header.spp_version	    = (raw_header[0] & 0xE0) >> 5
    primary_header.packet_type 	    = (raw_header[0] & 0x10) >> 4
    primary_header.sec_head_flag	= (raw_header[0] & 0x08) >> 3
    primary_header.apid	            = ((raw_header[0] & 0x03) << 8) | (raw_header[1])
    primary_header.seq_flags		= (raw_header[2] & 0xC0) >> 6
    primary_header.sc	            = ((raw_header[2] & 0x3F) << 8) | (raw_header[3])
    primary_header.data_len		    = (raw_header[4] << 8) | (raw_header[5])
    return primary_header