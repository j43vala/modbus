import asyncio
from pymodbus.client import AsyncModbusSerialClient 
from datetime import datetime
import time

async def async_read_modbus_data(client, com_port, slave_id, register_address, number_of_registers=2):
  
    try:
        result = await client.read_holding_registers(register_address, number_of_registers, slave=slave_id)
        if result.isError():
            print(f"Error reading Modbus data: {result}")
            return None
        else:
            data = result.registers
            print(data)
            return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
async def test(client,slave_id):
    print(slave_id)
    result = await client.read_holding_registers(register_address, 100, slave=slave_id)
    return result.registers

async def main(com_port, slave_id, register_address, number_of_registers):
    client = AsyncModbusSerialClient(method='rtu', port=com_port, stopbits=1, bytesize=8, parity='N', baudrate=9600)
    await client.connect()
    
    # 
    main_start = datetime.now()
    for i in range(100):
        start = datetime.now()
    
        result = await client.read_holding_registers(register_address, 124, slave=3)
        if result.isError():
            print(f"Error reading Modbus data: {result}")
            return None
        else:
            data = result.registers
            # print(data)
        
        # print(datetime.now() - start)
        # time.sleep(0.1)
        start = datetime.now()

        result = await client.read_holding_registers(register_address, 124, slave=1)
        if result.isError():
            print(f"Error reading Modbus data: {result}")
            return None
        else:
            data = result.registers
            # print(data)
        # print(datetime.now() - start)
    print(datetime.now() - main_start)

    # tasks = [
    #     test(client,1),
        
    #     test(client,3),
    # ]
   
    # results = await asyncio.gather(*tasks)
    # print(results)
    # Disconnect from the Modbus server
    if client is not None:
        print("\n\n\n\n",client)
        client.close()
   
if __name__ == "__main__":
    com_port = '/dev/ttyUSB0'  # Update this with your actual COM port
    slave_id = 1  # Update this with your actual slave ID
    register_address = 150  # Update this with the register address you want to read
    number_of_registers = 100  # Update this with the number of registers to read
    
    asyncio.run(main(com_port, slave_id, register_address, number_of_registers), debug=True)

# import asyncio
# # from pymodbus.client.async import ModbusSerialClient
# from pymodbus.client import AsyncModbusSerialClient as ModbusSerialClient

# import sqlite3

# # Function to read data from a Modbus slave
# async def read_data(client, slave_id, register_address):
#     result = await client.read_holding_registers(register_address, 100, unit=slave_id)
#     return result.registers

# # Function to store data in the database
# def store_in_database(slave_id, register_address, data):
#     # Replace this with your actual database handling code
#     connection = sqlite3.connect('your_database.db')
#     cursor = connection.cursor()
    
#     # Assuming you have a table named 'modbus_data'
#     cursor.execute("INSERT INTO modbus_data (slave_id, register_address, data) VALUES (?, ?, ?)",
#                    (slave_id, register_address, data))
    
#     connection.commit()
#     connection.close()

# # Main asynchronous function
# async def main():
#     # Create a Modbus serial client
#     client = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600)

#     # Connect to the Modbus server
#     await client.connect()

#     # List of tasks for reading data from multiple slaves and registers
#     tasks = [
#         read_data(client, 1, 100),
        
#         # read_data(client, 3, 100),
       
#     ]

#     # Execute tasks concurrently
#     results = await asyncio.gather(*tasks)

#     # Store the results in the database
#     # for i, result in enumerate(results):
#     #     slave_id = 1 if i < 3 else 3
#     #     register_address = [100, 200, 300][i % 3]
#     #     store_in_database(slave_id, register_address, result)

#     # Disconnect from the Modbus server
#     client.close()

# # Run the asyncio event loop
# asyncio.run(main())
