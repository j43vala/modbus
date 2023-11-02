from pymodbus.client import ModbusSerialClient

# Define the serial port settings
serial_port = '/dev/ttyUSB0'  # Replace with your actual serial port
baud_rate = 9600
timeout = 1

# Define Modbus address of your energy meter (change this to your device's address)
meter_address = 1

# Define the range of Modbus registers you want to read
start_register = 100  # Adjust the start register address
num_registers = 60
 # Adjust the number of registers to read

# Create a Modbus client
client = ModbusSerialClient(
    method='rtu',
    port=serial_port,
    baudrate=baud_rate,
    timeout=timeout,
)

# Open the serial connection
if not client.connect():
    print("Failed to connect to the Modbus device.")
else:
    try:
        values = client.read_holding_registers(start_register, num_registers, slave=meter_address)
        if values:
            for i, value in enumerate(values.registers):
                print(f"Register {start_register + i}: {value}")
        else:
            print("No response from the device.")
    except Exception as e:
        print(f"Error reading Modbus data: {str(e)}")

    # Close the serial connection
    client.close()
