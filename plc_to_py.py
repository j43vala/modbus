
import minimalmodbus
import time

# Define the COM port (adjust the port name as needed, e.g., 'COM1', 'COM2', etc.)
com_port = '/dev/ttyUSB0'

# Define the Modbus slave address (typically 1 for the first device)
slave_address = 1

# Create a Modbus instrument instance for your device
instrument = minimalmodbus.Instrument(com_port, slave_address)

# Set the Modbus serial communication parameters (baudrate, parity, etc.)
instrument.serial.baudrate = 9600 # Adjust to match your device's settings
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 2

# Define the Modbus function code and register address to read from
function_code = 3 # Read Holding Registers
register_addresses = [1, 2, 3, 4, 5]

# Define the number of registers to read
number_of_registers = 5 # Adjust based on your requirements

# Initialize the previous data
previous_data = None

while True:
  try:
# Read data from the Modbus device
     data = instrument.read_registers(register_addresses[0], number_of_registers, functioncode=function_code)

# Check if the data has changed
     if data != previous_data:
        print(f"Updated data:")
        for i in range(len(data)):
         print(f"Read data from register {register_addresses[i]}: {data[i]}")

# Update the previous data
     previous_data = data

# Wait for 5 seconds before reading again
     time.sleep(5)
  except Exception as e:
   print(f"An error occurred: {e}")

  finally:
# Close the serial connection
   instrument.serial.close()
