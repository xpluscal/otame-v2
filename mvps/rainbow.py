import opc
import time
import math
import colorsys

# Constants
NUM_LEDS = 256
SPEED = 0.1

def rainbow_animation(position):
    """Generates a rainbow color for a given position using a sine wave."""
    r = (math.sin(position + 0) * 127.5 + 127.5)
    g = (math.sin(position + 2) * 127.5 + 127.5)
    b = (math.sin(position + 4) * 127.5 + 127.5)
    return (int(r), int(g), int(b))

def generate_rainbow_frame(offset):
    """Generate a frame of rainbow colors with an offset."""
    return [rainbow_animation((i + offset) * SPEED) for i in range(NUM_LEDS)]

def main():
    client = opc.Client('localhost:7890')
    if not client.can_connect():
        print('ERROR: Cannot connect to Fadecandy server at localhost:7890')
        return

    print('Connected to Fadecandy server at localhost:7890')

    offset = 0
    try:
        while True:
            # Generate a frame of rainbow colors
            pixels = generate_rainbow_frame(offset)

            # Send the pixel values to the Fadecandy server
            client.put_pixels(pixels)
            
            # Increment the offset to create the animation effect
            offset += 1

            # Small delay to control the animation speed
            time.sleep(0.03)
    except KeyboardInterrupt:
        print("\nStopping animation...")
        client.put_pixels([(0,0,0)] * NUM_LEDS)  # Turn off all LEDs

if __name__ == "__main__":
    main()
