import opc
import time

# Create a client object
client = opc.Client('localhost:7890')

# Check if the client is connected
if client.can_connect():
    print('connected to %s' % client)

    # Make all pixels red
    pixels = [(255, 0, 0)] * 256 # Assuming you have 64 LEDs connected.
    client.put_pixels(pixels)
    time.sleep(10) # Let it display for a second
else:
    # We're not connected; print an error message
    print('WARNING: could not connect to %s' % client)

