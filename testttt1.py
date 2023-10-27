import struct
import minimalmodbus
def get_float(reg1 =  63317,reg2 = 17266):
    # 01000001 10100100 10011111 10111110 
    # 20.578

    combined_value = (reg2 << 16) | reg1

    # print(combined_value)

    float_value = struct.unpack('<f', struct.pack('<I', combined_value))[0]

    # print(struct.unpack('<f', struct.pack('<I', combined_value)))
    # print(float_value)


    # my_float = float(combined_value)

    # import bitstring
    # f1 = bitstring.BitArray(float=my_float, length=32)
    # f2 = bitstring.BitArray(float=float_value, length=32)
    # print(f1.bin)
    # print(f2.bin)
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



# if __name__ == "__main__":
#     my_float = get_float(reg2=123,reg1=345) 
#     print(my_float)
#     pass
import minimalmodbus
# import struct 
def read_data():
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
    instrument.serial.stopbits = 1

    function_code = 3  # Read Analog Output Holding Registers

    value = instrument.read_registers(140,4, function_code)
    print(value)


# def read_modbusdata(com_port, slave_id, registers):
#     instrument = minimalmodbus.Instrument(com_port, slave_id)
#     instrument.serial.baudrate = 9600
#     instrument.serial.bytesize = 8
#     instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
#     instrument.serial.stopbits = 2

#     function_code = 3  # Read Analog Output Holding Registers

#     data = []

#     for register in registers:
#         try:
#             value = instrument.read_register(register, function_code)
#             data.append(value)
#         except Exception as e:
#             print(f"Failed to read register {register}: {str(e)}")

#     return data

# if __name__ == "__main__":
#     # com_port = '/dev/ttyUSB0'  # Update this with your actual COM port
#     # slave_id = 1  # Update this with your actual slave ID
#     # registers_to_read = [101]  # Add the register addresses you want to read

#     # data = read_modbusdata(com_port, slave_id, registers_to_read)

#     # for register, value in zip(registers_to_read, data):
#     #     print(f"Register {register}: {value}")

#     # if len(data) == 2:
#     #     reg1, reg2 = data
#     #     combined_value = (reg2 << 16) | reg1
#     #     float_value = struct.unpack('<f', struct.pack('<I', combined_value))[0]
#     #     print(f"Converted Float Value: {float_value}")   
#     read_data()


from pymodbus.client import ModbusSerialClient as ModbusClient

# from pymodbus.client import ModbusSerialClient

# def run():
#     client = ModbusSerialClient("dev/serial0")

#     client.connect()
#     ...
#     client.close()
def read_modbus_data(com_port, slave_id, register_address, number_of_registers):
    client = ModbusClient(method='rtu', port=com_port, stopbits=1, bytesize=8, parity='N', baudrate=9600)

    client.connect()

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
    finally:
        client.close()
    # client.close()

# def read_modbus_data(com_port, slave_id, register_address, number_of_registers):
#     client = ModbusClient(method='rtu', port=com_port, stopbits=1, bytesize=8, parity='N', baudrate=9600)
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
    register_address = 138  # Update this with the register address you want to read
    number_of_registers = 20  # Update this with the number of registers to read

    data = read_modbus_data(com_port, slave_id, register_address, number_of_registers)

    if data is not None:
        print(f"Data read from Modbus: {data}")
    print(get_float())
