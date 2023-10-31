import opc
import time
import math
import random

# Configuration
MATRIX_SIZE = 8
HALF_MATRIX = MATRIX_SIZE // 2
TOTAL_MATRICES = 4
LEDS_PER_MATRIX = 64
TOTAL_LEDS = LEDS_PER_MATRIX * TOTAL_MATRICES
SPEED_FACTOR = 4.0  # Increases the speed of the animation
COLOR_CHANGE_SPEED = 0.5  # Controls the speed of color change
NOISE_FACTOR = 0.1  # Intensity of the noise for color variation

# Create a client object
client = opc.Client('localhost:7890')

# Function to calculate distance from the center of a matrix
def distance_from_center(x, y):
    dx = x - HALF_MATRIX + 0.5
    dy = y - HALF_MATRIX + 0.5
    return math.sqrt(dx**2 + dy**2)

def hsb_to_rgb(h, s, b):
    """Convert HSB/HSV values to RGB colors."""
    import colorsys
    r, g, b = colorsys.hsv_to_rgb(h, s, b)
    return int(r * 255), int(g * 255), int(b * 255)

try:
    # Main animation loop
    while True:
        pixels = []

        # Get the current time to use as an animation factor
        t = time.time() * SPEED_FACTOR

        color_shift = (math.sin(t * COLOR_CHANGE_SPEED) + 1) / 2  # produces values between 0 and 1

        hue_shift = color_shift * 0.25  # Only transition from red (0) to purple (0.25) to blue (0.5)

        # Loop over matrices
        for matrix_num in range(TOTAL_MATRICES):
            matrix_offset_x = (matrix_num % 2) * MATRIX_SIZE
            matrix_offset_y = (matrix_num // 2) * MATRIX_SIZE

            for y in range(MATRIX_SIZE):
                for x in range(MATRIX_SIZE):
                    adjusted_x = x + matrix_offset_x
                    adjusted_y = y + matrix_offset_y

                    distance = distance_from_center(adjusted_x % 8, adjusted_y % 8)

                    brightness = (math.sin(t - distance) + 1) / 2  # produces values between 0 and 1
                    hue_variance = random.uniform(-NOISE_FACTOR, NOISE_FACTOR)
                    hue = hue_shift + hue_variance

                    r, g, b = hsb_to_rgb(hue, 1, brightness)

                    pixels.append((r, g, b))

        # Send pixels to Fadecandy
        client.put_pixels(pixels)

        # Wait for a short period of time before the next frame
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Interrupted by user. Exiting...")
    # Turn off all LEDs
    client.put_pixels([(0, 0, 0)] * TOTAL_LEDS)
