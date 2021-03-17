import socket

class conn_plpc:
    def  __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn_class = self.connect_init()

    def connect_init(self):
        conn_class = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_class.connect((self.host, self.port))
        return conn_class
    
    def plc_comm(self, company_id, request, dtype, headdevice, values = '0'):
        header = makeHeader(company_id)  
        app_instruction = makeInstruction(request, dtype, headdevice, values)
        update_header = updateHeader(header, app_instruction)
        retByte = update_header + app_instruction
        conn_class = self.conn_class
        conn_class.send(retByte)
        if request == 'read':
            val_temp = conn_class.recv(1024)
            val = val_temp[-1]
            return val

def makeHeader(company_id):
    header = bytearray(b'')
    if company_id == 'XGT' or company_id == 'XGB':
        company_header = bytearray(b'LSIS-XGT') # 8bytes 
        company_header = company_header + bytearray(b'\x00\x00') # for reservation: total 10bytes
    else:
        company_header = bytearray(b'LGIS-GLOFA') # 10bytes
    plc_header = bytearray(b'\x00\x00') # Don't care
    cpu_header = bytearray(b'\x00')
    src_frame_header = bytearray(b'\x33') # send PC to PLC
    invoke_id_header = bytearray(b'\x00\x00') # for error check
    header = company_header + plc_header + cpu_header + src_frame_header + invoke_id_header # make init header
    return header

def updateHeader(header, app_instruction):
    len_header =  bytes([len(app_instruction), 0]) # instruction length
    fenet_header = bytearray(b'\x00') # Don't care
    reserved_header = bytearray(b'\x00') # Don't care
    update_header = header + len_header + fenet_header + reserved_header
    print("update header: ", update_header)
    return update_header

def makeInstruction(request, dtype, headdevice, values='0'):
    # for find data num & split head device name
    tmp_headdevice = headdevice.split(',') 
    data_count = len(tmp_headdevice)
    # data type
    if dtype == 'bit':
        dtype_instruction = bytearray(b'\x00\x00')
    elif dtype == 'byte':
        dtype_instruction = bytearray(b'\x01\x00')
    elif dtype == 'word':
        dtype_instruction = bytearray(b'\x02\x00')
    elif dtype == 'dword':
        dtype_instruction = bytearray(b'\x03\x00')
    elif dtype == 'lword':
        dtype_instruction = bytearray(b'\x04\x00')
    else:
        dtype_instruction = bytearray(b'\x14\x00')

    reserved_instruction = bytearray(b'\x00\x00') # reservation area
    num_instruction = bytes([data_count, 0]) # data count
    data_instructions = bytearray(b'')
    for i in range(data_count):
        data_instruction = bytearray(b'')
        data_instruction = data_instruction + str2hqx('%')
        if tmp_headdevice[i][0] == 'P':
            pass
            # data_instruction = data_instruction + str2hqx('M')
        elif tmp_headdevice[i][0] == 'M':
            data_instruction = data_instruction + str2hqx('M')
        elif tmp_headdevice[i][0] == 'L':
            # data_instruction = data_instruction + str2hqx('M')
            pass
        elif tmp_headdevice[i][0] == 'F':
            # data_instruction = data_instruction + str2hqx('M')
            pass
        elif tmp_headdevice[i][0] == 'K':
            # data_instruction = data_instruction + str2hqx('M')
            pass
        elif tmp_headdevice[i][0] == 'C':
            # data_instruction = data_instruction + str2hqx('M')
            pass
        elif tmp_headdevice[i][0] == 'D':
            # data_instruction = data_instruction + str2hqx('M')
            pass
        elif tmp_headdevice[i][0] == 'T':
            # data_instruction = data_instruction + str2hqx('M')
            pass
        elif tmp_headdevice[i][0] == 'N':
            # data_instruction = data_instruction + str2hqx('M')
            pass
        elif tmp_headdevice[i][0] == 'R':
            # data_instruction = data_instruction + str2hqx('M')
            pass
        
        if dtype == 'bit': 
            data_instruction = data_instruction + str2hqx('X')
        elif dtype == 'byte':
            # data_instruction = data_instruction + str2hqx('X')
            pass
        elif dtype == 'word':
            # data_instruction = data_instruction + str2hqx('X')
            pass
        elif dtype == 'dword':
            # data_instruction = data_instruction + str2hqx('X')
            pass
        elif dtype == 'lword':
            # data_instruction = data_instruction + str2hqx('X')
            pass
        variable_instruction = bytearray(b'')
        for j in range(len(tmp_headdevice[i])-1):
            variable_instruction = variable_instruction + str2hqx(tmp_headdevice[i][j+1])
        len_instruction = bytes([len(data_instruction) + len(variable_instruction), 0]) # length of variable name
        data_instructions = data_instructions + len_instruction + data_instruction + variable_instruction
    # read or write
    if request == 'read':
        print("Request Read")
        request_instruction = bytearray(b'\x54\x00') # read
        final_instruction = request_instruction + dtype_instruction + reserved_instruction + num_instruction + data_instructions
    else:
        print("Request Write")
        request_instruction = bytearray(b'\x58\x00') # write
        value_instruction = bytearray(b'')
        values = values.split(',') 
        for value in values:
            temp_value = mk_value(int(value))
            value_instruction = value_instruction + temp_value
        final_instruction = request_instruction + dtype_instruction + reserved_instruction + num_instruction + data_instructions + value_instruction
    print("app_instruction: ", final_instruction)
    return final_instruction

def mk_value(value): # need to update for bit, word etc ...
    temp_value = bytes([1, 0, value])
    return temp_value

def str2hqx(string):
    if string == '0':
        hqx = bytearray(b'\x30')
    elif string == '1':
        hqx = bytearray(b'\x31')
    elif string == '2':
        hqx = bytearray(b'\x32')
    elif string == '3':
        hqx = bytearray(b'\x33')
    elif string == '4':
        hqx = bytearray(b'\x34')
    elif string == '5':
        hqx = bytearray(b'\x35')
    elif string == '6':
        hqx = bytearray(b'\x36')
    elif string == '7':
        hqx = bytearray(b'\x37')
    elif string == '8':
        hqx = bytearray(b'\x38')
    elif string == '9':
        hqx = bytearray(b'\x39')
    elif string == '%':
        hqx = bytearray(b'\x25')
    elif string == 'M':
        hqx = bytearray(b'\x4d')
    elif string == 'X':
        hqx = bytearray(b'\x58')
    return hqx

    # def plc2pc_get_val(self, read_size=1, headdevice="D701"):
    #     retByte = b'\x4C\x53\x49\x53\x2D\x58\x47\x54\x00\x00\x00\x00\x00\x33\x00\x00\x10\x00\x00\x00\x54\x00\x00\x00\x00\x00\x01\x00\x06\x00\x25\x4D\x58\x37\x30\x31'
    #     conn_class = self.conn_class
    #     conn_class.send(retByte)
    #     val_temp = conn_class.recv(1024)
    #     val = val_temp[-1]
    #     return val
    
    # def plc2pc_check_val(self, check_val, headdevice="D700"):
    #     conn_class = self.conn_class
    #     retByte = b'\x4C\x53\x49\x53\x2D\x58\x47\x54\x00\x00\x00\x00\x00\x33\x00\x00\x10\x00\x00\x00\x54\x00\x00\x00\x00\x00\x01\x00\x06\x00\x25\x4D\x58\x37\x30\x30'
    #     while True:
    #         conn_class.send(retByte)
    #         val_temp = conn_class.recv(1024)
    #         val = val_temp[-1]
    #         if val == check_val:
    #             return True
    #     return False

    # def pc2plc(self, values, headdevice="D700"):
    #     if values == 1:
    #         conn_class = self.conn_class
    #         retByte = b'\x4C\x53\x49\x53\x2D\x58\x47\x54\x00\x00\x00\x00\x00\x33\x00\x00\x34\x00\x00\x00\x58\x00\x00\x00\x00\x00\x04\x00\x06\x00\x25\x4D\x58\x37\x30\x30\x06\x00\x25\x4D\x58\x37\x30\x31\x06\x00\x25\x4D\x58\x37\x30\x32\x06\x00\x25\x4D\x58\x37\x30\x33\x01\x00\x01\x01\x00\x00\x01\x00\x00\x01\x00\x00'
    #         conn_class.send(retByte)
    #     # response = conn_class.recv(1024)
if __name__ == '__main__':
    PLC_INFORM = {
    'host':"192.168.1.10",
    'port':2004
    }
    conn = conn_plpc(**PLC_INFORM)
    val = conn.plc_comm('XGT','read','bit','M750,M751,M752')
    print(val)