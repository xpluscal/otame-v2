import opc
import time
import math

NUM_LEDS = 128
ADDRESS = 'localhost:7890'

def wave_effect(position, total, color, width=5):
    # Create a "wave" effect for a given position in a total number of LEDs.
    # Width determines how wide the wave appears.
    midpoint = float(position) / total
    value = (math.sin(time.time() + (midpoint * width * math.pi)) + 1) / 2
    return tuple([int(c * value) for c in color])

def main():
    client = opc.Client(ADDRESS)

    if not client.can_connect():
        print('Cannot connect to the server at {0}. Exiting.'.format(ADDRESS))
        return
    
    print('Connected to {0}.'.format(ADDRESS))
    color = (255, 0, 127)  # Initial color (pinkish)

    try:
        while True:
            pixels = [wave_effect(i, NUM_LEDS, color) for i in range(NUM_LEDS)]
            client.put_pixels(pixels)
            time.sleep(0.1)  # Adjust this to make the wave move faster or slower
    except KeyboardInterrupt:
        print('Animation interrupted. Exiting...')
        pixels = [(0, 0, 0)] * NUM_LEDS
        client.put_pixels(pixels)

if __name__ == '__main__':
    main()
