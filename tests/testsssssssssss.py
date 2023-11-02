# # # import mysql.connector

# # # # Replace these with your own database credentials
# # # host = "192.168.1.18"
# # # # port= 3306
# # # user = "wzero"
# # # password = "wzero123"
# # # database = "plc"

# # # # Create a connection to the MySQL server
# # # try:
# # #     connection = mysql.connector.connect(
# # #         host=host,
# # #         user=user,
# # #         password=password,
# # #         database=database
# # #     )
    
# # #     if connection.is_connected():
# # #         print("Connected to MySQL database")
        
# # #         # You can now perform database operations here
        
# # # except mysql.connector.Error as error:
# # #     print("Error connecting to MySQL database:", error)
# # # finally:
# # #     # Close the connection when you're done
# # #     if 'connection' in locals():
# # #         connection.close()
# # #         print("MySQL connection is closed")

# # from pymodbus.client import ModbusSerialClient as ModbusClient
# # from pymodbus.constants import Endian
# # from pymodbus.payload import BinaryPayloadDecoder

# # # Replace this value with your PLC's serial port name (e.g., 'COM1' on Windows or '/dev/ttyUSB0' on Linux)
# # serial_port = '/dev/ttyUSB0'

# # # Replace this value with your PLC's slave ID
# # slave_id = 3

# # # Create a Modbus client instance for your PLC
# # client = ModbusClient(method='rtu', port=serial_port, stopbits=1, bytesize=8, parity="N", baudrate=9600)

# # # client = ModbusClient(method='rtu', port=serial_port, baudrate=9600)
# # client.connect()

# # # # Set the communication parameters (baudrate, parity, stopbits, etc.) if necessary
# # # instrument.serial.baudrate = 9600
# # # instrument.serial.bytesize = 8
# # # instrument.serial.parity = 'N'
# # # instrument.serial.stopbits = 2

# # # Read holding registers
# # start_address = 398  # Replace with the starting address of your holding register
# # num_registers = 10  # Replace with the number of registers you want to read

# # try:
# #      for i in range(num_registers):
# #         register_address = start_address + i
# #         # Read the registers
# #         result = client.read_holding_registers(register_address, 2, slave=slave_id)
# #         print('result: ', result)
# #         if not result.isError():
# #             register_value = result.registers[0]
# #             print(f"{register_address}={register_value}")


# #             # BinaryPayloadDecoder to decode the raw data if needed
# #             # decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Little) 
# #             # decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Little)
            
# #             decoder = BinaryPayloadDecoder(payload)
# #             first   = decoder.decode_8bit_uint()
# #             second  = decoder.decode_16bit_uint()

# #             # Example: decode a 32-bit value
# #             decoded_value = decoder.decode_8bit_int()
# #             print(f"Decoded Value: {decoded_value}")
# #         else:
            
# #             print(f"Failed to read register {register_address}", result.isError())
        

# # except Exception as e:
# #     print(f"Failed to read holding registers: {str(e)}")

# # # Close the serial connection
# # client.close()

reg1 = 50000000
reg2 = 115568000

# Combine the 32-bit double integer values
combined_value = (reg1 << 16) | (reg2 & 0xFFFF)

# Print the result as a combined 32-bit double integer
print(combined_value)
# from pymodbus.client import ModbusSerialClient as ModbusClient
# from pymodbus.constants import Endian
# from pymodbus.payload import BinaryPayloadDecoder
# import struct  # Import the struct module

# # Replace this value with your PLC's serial port name (e.g., 'COM1' on Windows or '/dev/ttyUSB0' on Linux)
# serial_port = '/dev/ttyUSB0'

# # Replace this value with your PLC's slave ID
# slave_id = 3

# # Create a Modbus client instance for your PLC
# client = ModbusClient(method='rtu', port=serial_port, stopbits=2, bytesize=8, parity="N", baudrate=9600, timeout=5)
# client.connect()

# # Read holding registers
# start_address = 398  # Replace with the starting address of your holding register
# num_registers = 10  # Replace with the number of registers you want to read

# try:
#     for i in range(num_registers):
#         register_address = start_address + i
#         # Read the registers
#         result = client.read_holding_registers(register_address, 2, slave=slave_id)
#         # print('result: ', result)
#         if not result.isError():
#             register_value = result.registers[0]
#             print(f"{register_address} = {register_value}")

#             # Convert the list of registers to bytes using struct
#             payload = struct.pack('>' + 'H' * len(result.registers), *result.registers)

#             # Use BinaryPayloadDecoder to decode the raw data
#             decoder = BinaryPayloadDecoder(payload, byteorder=Endian.LITTLE, wordorder=Endian.LITTLE)

#             # Example: decode an 8-bit unsigned integer (uint8)
#             first = decoder.decode_8bit_uint()

#             # Example: decode a 16-bit unsigned integer (uint16)
#             second = decoder.decode_16bit_uint()

#             # Example: decode a 8-bit signed integer (int8)
#             decoded_value_int8 = decoder.decode_8bit_int()

#         else:
#             print(f"Failed to read register {register_address}, Error: {result}")
# except Exception as e:
#     print(f"Failed to read holding registers: {str(e)}")

# # Close the serial connection
# client.close()
