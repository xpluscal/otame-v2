import opc
import time
import math

# Configuration
MATRIX_SIZE = 8
HALF_MATRIX = MATRIX_SIZE // 2
TOTAL_MATRICES = 4
LEDS_PER_MATRIX = 64
TOTAL_LEDS = LEDS_PER_MATRIX * TOTAL_MATRICES
SPEED_FACTOR = 4.0  # Increases the speed of the animation
COLOR_CHANGE_SPEED = 0.5  # Controls the speed of color change

# Create a client object
client = opc.Client('localhost:7890')

# Function to calculate distance from the center of a matrix
def distance_from_center(x, y):
    dx = x - HALF_MATRIX + 0.5
    dy = y - HALF_MATRIX + 0.5
    return math.sqrt(dx**2 + dy**2)

try:
    # Main animation loop
    while True:
        pixels = []

        # Get the current time to use as an animation factor
        t = time.time() * SPEED_FACTOR
        color_shift = (math.sin(t * COLOR_CHANGE_SPEED) + 1) / 2  # produces values between 0 and 1

        # Loop over matrices
        for matrix_num in range(TOTAL_MATRICES):
            matrix_offset_x = (matrix_num % 2) * MATRIX_SIZE
            matrix_offset_y = (matrix_num // 2) * MATRIX_SIZE

            for y in range(MATRIX_SIZE):
                for x in range(MATRIX_SIZE):
                    adjusted_x = x + matrix_offset_x
                    adjusted_y = y + matrix_offset_y
                    
                    distance = distance_from_center(adjusted_x % 8, adjusted_y % 8)
                    
                    # Calculate a brightness value using the sine function to create the ripple effect
                    brightness = (math.sin(t - distance) + 1) / 2  # produces values between 0 and 1

                    # Interpolate between red and blue based on color_shift value
                    r = int(255 * brightness * color_shift)
                    g = 0
                    b = int(255 * brightness * (1 - color_shift))

                    pixels.append((r, g, b))

        # Send pixels to Fadecandy
        client.put_pixels(pixels)

        # Wait for a short period of time before the next frame
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Interrupted by user. Exiting...")
    # Turn off all LEDs
    client.put_pixels([(0, 0, 0)] * TOTAL_LEDS)
