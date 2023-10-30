from pymodbus.client import ModbusSerialClient
import struct
from datetime import datetime



def get_float(reg1 =  63317,reg2 = 17266):
    # 01000001 10100100 10011111 10111110 
    # 20.578
    combined_value = (reg2 << 16) | reg1
    # print(combined_value)

    float_value = struct.unpack('<f', struct.pack('<I', combined_value))[0]

    return float_value

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
    slave_id = 1  # Update this with your actual slave ID
    register_address = 150  # Update this with the register address you want to read
    number_of_registers = 126  # Update this with the number of registers to read
    
    client = ModbusSerialClient(method='rtu', port=com_port, stopbits=1, bytesize=8, parity='N', baudrate=9600)
    client.connect()

    # read data in single request
    start = datetime.now()
    data = read_modbus_data(client,com_port, slave_id, register_address, number_of_registers)
    print(data)
    print("time taken for single read", datetime.now() - start)
    
    # # read data in multiple request
    # start = datetime.now()
    # curr_reg = register_address
    # while curr_reg <= register_address + number_of_registers:
    #     data = read_modbus_data(client, com_port, slave_id, register_address, 2)
    #     curr_reg += 2
    #     # print(data)
    
    # print("time taken for multi read", datetime.now() - start)
    # print("curr_reg ", curr_reg)

    start = datetime.now()
    for i in range(100):
        data = read_modbus_data(client,com_port, 1, register_address, 2)
        data = read_modbus_data(client,com_port, 3, register_address, 2)

    print("time taken for 2 reg 100 times", datetime.now() - start)
    
    start = datetime.now()
    for i in range(10):
        data = read_modbus_data(client,com_port, 1, register_address, 10)
        data = read_modbus_data(client,com_port, 3, register_address, 10)

    print("time taken for 10 reg 10 times", datetime.now() - start)

    
    start = datetime.now()
    for i in range(10):
        data = read_modbus_data(client,com_port, 1, register_address, 100)
        data = read_modbus_data(client,com_port, 3, register_address, 100)

    print("time taken for 100 reg 10 times", datetime.now() - start)

    start = datetime.now()
    for i in range(100):
        data = read_modbus_data(client,com_port, 1, register_address, 10)
        data = read_modbus_data(client,com_port, 3, register_address, 10)

    print("time taken for 10 reg 100 times", datetime.now() - start)
    
    start = datetime.now()
    for i in range(100):
        data = read_modbus_data(client,com_port, 1, register_address, 100)
        data = read_modbus_data(client,com_port, 3, register_address, 100)

    print("time taken for 100 reg 100 times", datetime.now() - start)
    
    client.close()
    
    # if data is not None:
    #     print(f"Data read from Modbus: {data}")
    # print(get_float())


    
    
    