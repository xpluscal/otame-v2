import opc
import time
import math
import random

# Configuration
MATRIX_SIZE = 8
TOTAL_LEDS_MATRIX = MATRIX_SIZE * MATRIX_SIZE
TOTAL_LEDS_STRIP = 64
TOTAL_LEDS = TOTAL_LEDS_MATRIX + TOTAL_LEDS_STRIP
CENTER_X, CENTER_Y = MATRIX_SIZE // 2, MATRIX_SIZE // 2
NOISE_FACTOR = 0.1
RIPPLE_SPEED = 0.15
WATERFALL_SPEED = 0.9
SPEED_VARIANCE = 0.25  # This will add variance to the speed of each iteration.

client = opc.Client('localhost:7890')  # Initialize the Fadecandy client

def hue_to_rgb(hue):
    r = int(255 * (1 - hue))
    b = int(255 * hue)
    return r, 0, b

def ripple_value(dist, t):
    """Calculate ripple value based on distance and time."""
    value = (1 + math.sin(dist - t * (1 + random.uniform(-SPEED_VARIANCE, SPEED_VARIANCE)))) / 2
    return value

def waterfall_value(i, t):
    """Calculate waterfall value based on index and time."""
    value = (1 + math.sin((TOTAL_LEDS_STRIP - i) - t)) / 2  # Reversed direction
    return value

def main():
    t = 0
    try:
        while True:
            pixels = []

            # Calculate pixels for matrix
            for i in range(MATRIX_SIZE):
                for j in range(MATRIX_SIZE):
                    dist = math.sqrt((CENTER_X - i)**2 + (CENTER_Y - j)**2)
                    brightness = ripple_value(dist, t)

                    hue = (math.sin(time.time() * 0.05) + 1) / 2  # Hue oscillates between 0 and 1
                    hue += random.uniform(-NOISE_FACTOR, NOISE_FACTOR)
                    hue = max(0, min(hue, 1))  # Ensure hue remains within [0, 1]

                    r, g, b = hue_to_rgb(hue)
                    pixels.append((int(r * brightness), int(g * brightness), int(b * brightness)))

            # Calculate pixels for strip
            for i in range(TOTAL_LEDS_STRIP):
                brightness = waterfall_value(i, t * WATERFALL_SPEED)
                hue = (math.sin(time.time() * 0.05 + i * 0.02) + 1) / 2  # Offset hue based on position
                r, g, b = hue_to_rgb(hue)
                pixels.append((int(r * brightness), int(g * brightness), int(b * brightness)))

            client.put_pixels(pixels)
            time.sleep(0.05)
            t += RIPPLE_SPEED
    except KeyboardInterrupt:
        pixels = [(0, 0, 0)] * TOTAL_LEDS
        client.put_pixels(pixels)  # Turn off LEDs when stopping the script

if __name__ == "__main__":
    main()
