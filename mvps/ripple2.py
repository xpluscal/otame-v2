import opc
import time
import math
import random

# Configuration
MATRIX_SIZE = 8
TOTAL_LEDS = MATRIX_SIZE * MATRIX_SIZE * 2
CENTER_X, CENTER_Y = MATRIX_SIZE // 2, MATRIX_SIZE // 2
NOISE_FACTOR = 0.1  # The amount of hue noise; adjust as needed

client = opc.Client('localhost:7890')  # Initialize the Fadecandy client

def hue_to_rgb(hue):
    r = int(255 * (1 - hue))
    b = int(255 * hue)
    return r, 0, b

def ripple_value(dist, t):
    """Calculate ripple value based on distance and time."""
    value = (1 + math.sin(dist - t)) / 2
    return value

def main():
    t = 0
    try:
        while True:
            pixels = []

            for i in range(MATRIX_SIZE):
                for j in range(MATRIX_SIZE):
                    dist = math.sqrt((CENTER_X - i)**2 + (CENTER_Y - j)**2)
                    brightness = ripple_value(dist, t)

                    hue = (time.time() * 0.05) % 1  # Slowly shift hue over time

                    # Introduce some hue noise
                    hue += random.uniform(-NOISE_FACTOR, NOISE_FACTOR)
                    hue = max(0, min(hue, 1))  # Ensure hue remains within [0, 1]

                    r, g, b = hue_to_rgb(hue)
                    pixels.append((int(r * brightness), int(g * brightness), int(b * brightness)))

            client.put_pixels(pixels)
            time.sleep(0.05)
            t += 0.1
    except KeyboardInterrupt:
        pixels = [(0, 0, 0)] * TOTAL_LEDS
        client.put_pixels(pixels)  # Turn off LEDs when stopping the script

if __name__ == "__main__":
    main()
