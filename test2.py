import opc
import time

# Create a client object for OPC connection
client = opc.Client('localhost:7890')

# Check if the client is connected
if client.can_connect():
    print('Connected to the OPC server.')
else:
    print('WARNING: Could not connect to the OPC server.')
    exit()

# Initialize an array of off pixels (black)
pixels = [(0, 0, 0)] * 256

# Light up the first LED in the first matrix with red
pixels[0] = (255, 0, 0)

# Send this to the OPC server
client.put_pixels(pixels)

# Pause to see the LED
time.sleep(10)
