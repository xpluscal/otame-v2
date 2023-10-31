import opc
import time
import math
import random

# Configuration
MATRIX_SIZE = 8
TOTAL_LEDS_MATRIX = MATRIX_SIZE * MATRIX_SIZE
TOTAL_LEDS_STRIP = 64
TOTAL_LEDS = TOTAL_LEDS_MATRIX + TOTAL_LEDS_STRIP
NOISE_FACTOR = 0.2
RIPPLE_SPEED = 0.10
SPEED_VARIANCE = 0.05  # This will add variance to the speed of each iteration.

client = opc.Client('localhost:7890')  # Initialize the Fadecandy client

def hue_to_rgb(hue):
    r = int(255 * (1 - hue))
    b = int(255 * hue)
    return r, 0, b

def lerp(start, end, fraction):
    return start + fraction * (end - start)

def ripple_value(dist, t):
    """Calculate ripple value based on distance and time."""
    value = (1 + math.sin(dist - t * (1 + random.uniform(-SPEED_VARIANCE, SPEED_VARIANCE)))) / 2
    return value

def main():
    t = 0
    CENTER_X, CENTER_Y = MATRIX_SIZE // 2, MATRIX_SIZE // 2
    TARGET_X, TARGET_Y = random.randint(0, MATRIX_SIZE-1), random.randint(0, MATRIX_SIZE-1)

    try:
        while True:
            if t == 0:
                TARGET_X, TARGET_Y = random.randint(0, MATRIX_SIZE-1), random.randint(0, MATRIX_SIZE-1)

            pixels = []
            
            # Calculate the current center point
            current_center_x = lerp(CENTER_X, TARGET_X, t / (2 * math.pi))
            current_center_y = lerp(CENTER_Y, TARGET_Y, t / (2 * math.pi))

            # Calculate pixels for both matrixes
            for matrix_index in range(2):  # One for the actual matrix and one for the strip
                for i in range(MATRIX_SIZE):
                    for j in range(MATRIX_SIZE):
                        dist = math.sqrt((current_center_x - i)**2 + (current_center_y - j)**2)
                        brightness = ripple_value(dist, t)

                        hue = (math.sin(time.time() * 0.05) + 1) / 2  # Hue oscillates between 0 and 1
                        hue += random.uniform(-NOISE_FACTOR, NOISE_FACTOR)
                        hue = max(0, min(hue, 1))  # Ensure hue remains within [0, 1]

                        r, g, b = hue_to_rgb(hue)
                        pixels.append((int(r * brightness), int(g * brightness), int(b * brightness)))

            client.put_pixels(pixels)
            time.sleep(0.05)
            t += RIPPLE_SPEED
            if t > 2 * math.pi:  # Complete one ripple cycle
                t = 0
                CENTER_X, CENTER_Y = TARGET_X, TARGET_Y  # Set the current center to the target for the next iteration
    except KeyboardInterrupt:
        pixels = [(0, 0, 0)] * TOTAL_LEDS
        client.put_pixels(pixels)  # Turn off LEDs when stopping the script

if __name__ == "__main__":
    main()
