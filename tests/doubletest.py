from pymodbus.client import ModbusSerialClient
import struct
from datetime import datetime



# def get_float(reg1 =  63317,reg2 = 17266):
def get_double(reg1 =  4621,reg2 = 3646):
    # 01000001 10100100 10011111 10111110 
    # 20.578

    
    # reg1 = reg1 if reg1 <= 0x7FFF else reg1 - 0x10000
    # reg2 = reg2 if reg2 <= 0x7FFF else reg2 - 0x10000


    reg1 = 0b0000000000000000 1000000000000000
    reg2 = 0b1000000000000000 0000000000000000
    # -------------------------------------------------
    res1 = 0b0000000000000000 1000000000000000 1000000000000000
    reg3 = 0b1000000000000000 0000000000000000 0000000000000000


    reg4 = 0b1000000000000000 1000000000000000 1000000000000000 1000000000000000

    # print(reg1, reg2)
    uint32 =    (reg4 << 48) | (reg3 << 32) | (reg2 << 16) | reg1
    print("uint32 :", uint32)
    print("uint32 :", bin(uint32))

    # Convert to a 32-bit signed integer
    int32 = uint32 & 0x7FFFFFFF  # Apply bitwise AND with 0x7FFFFFFF to clear the sign bit
    print("int32 without sign :", int32)
    print("int32 without sign :", bin(int32))
    # Check the sign bit (the most significant bit)
    # if (uint32 & 0x80000000) != 0:
    if (uint32 >> 31) == 1:
        int32 = -int32
    print("int32 with sign :", int32)
    print("int32 with sign :", bin(int32))


    # combined_value =  combined_value if combined_value < 0x80000000 else combined_value - 0x100000000
    print(int32)
    # print(combined_value)

    # float_value = struct.unpack('<f', struct.pack('<I', combined_value))[0]
    # double_value = struct.unpack('<l', struct.pack('<HH', reg1, reg2))[0]
    # print(double_value)

    # return float_value
    # return double_value
# def read_modbusdata(reg, number_of_reg = 1):

#      instrument = minimalmodbus.Instrument(/dev/ttyUSB0 , device.get("slave_id"))
#             instrument.serial.baudrate = 9600
#             instrument.serial.bytesize = 8
#             instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
#             instrument.serial.stopbits = 2

#             function_code = 3
#             register_dict = device.get("register")  # Use the addresses from the JSON file
#             number_of_registers = len(register_dict)

#             previous_data = None



def read_modbus_data(client, com_port, slave_id, register_address, number_of_registers=2):
  
    try:
        result = client.read_holding_registers(register_address, number_of_registers, slave=slave_id)
        if result.isError():
            print(f"Error reading Modbus data: {result}")
            return None
        else:
            data = result.registers
            return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# def read_modbus_data(com_port, slave_id, register_address, number_of_registers):
#     client = ModbusSerialClient(method='rtu', port=com_port, stopbits=1, bytesize=8, parity='N', baudrate=9600)
#     client.connect()

#     try:
#         result = client.read_holding_registers(register_address, number_of_registers, slave=slave_id)
#         if result.isError():
#             print(f"Error reading Modbus data: {result}")
#             return None
#         else:
#             reg_1, reg_2 = result.registers
#             data = get_float(reg_1, reg_2)
#             return data
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return None
#     finally:
#         client.close()

if __name__ == "__main__":

    com_port = '/dev/ttyUSB0'  # Update this with your actual COM port
    slave_id = 3  # Update this with your actual slave ID
    register_address = 404  # Update this with the register address you want to read
    number_of_registers = 126  # Update this with the number of registers to read
    
    client = ModbusSerialClient(method='rtu', port=com_port, stopbits=1, bytesize=8, parity='N', baudrate=9600)
    client.connect()
    data = read_modbus_data(client, com_port, slave_id, register_address, 2)
    print('data: ', data)
    

    get_double(*data)

