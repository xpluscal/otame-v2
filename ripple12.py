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
NOISE_TRANSITION_SPEED = 0.05  # Controls the smoothness of color noise transition
RIPPLE_NON_UNIFORMITY = 0.4  # Adjust this for more or less ripple distortion

# Create a client object
client = opc.Client('localhost:7890')

# Function to calculate distance from the center of a matrix
def distance_from_center(x, y, t):
    dx = x - HALF_MATRIX + 0.5
    dy = y - HALF_MATRIX + 0.5
    base_distance = math.sqrt(dx**2 + dy**2)
    
    # Add non-uniformity to the ripple
    non_uniform_factor = 1 + RIPPLE_NON_UNIFORMITY * math.sin(2 * math.pi * base_distance + t)
    return base_distance * non_uniform_factor

# Initialize a random color noise value for each LED
color_noises = [random.uniform(-0.1, 0.1) for _ in range(TOTAL_LEDS)]

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
                    
                    distance = distance_from_center(adjusted_x % 8, adjusted_y % 8, t)
                    
                    # Calculate a brightness value using the sine function to create the ripple effect
                    brightness = (math.sin(t - distance) + 1) / 2  # produces values between 0 and 1

                    # Adjust the color_shift for this LED using its noise value
                    led_idx = matrix_num * LEDS_PER_MATRIX + y * MATRIX_SIZE + x
                    led_color_shift = color_shift + color_noises[led_idx]

                    # Interpolate between red and blue based on led_color_shift value
                    r = int(255 * brightness * led_color_shift)
                    g = 0
                    b = int(255 * brightness * (1 - led_color_shift))

                    pixels.append((r, g, b))
                    
                    # Update the color noise for this LED
                    color_noises[led_idx] += random.uniform(-NOISE_TRANSITION_SPEED, NOISE_TRANSITION_SPEED)
                    color_noises[led_idx] = max(-0.1, min(0.1, color_noises[led_idx]))  # Clamp the value

        # Send pixels to Fadecandy
        client.put_pixels(pixels)

        # Wait for a short period of time before the next frame
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Interrupted by user. Exiting...")
    # Turn off all LEDs
    client.put_pixels([(0, 0, 0)] * TOTAL_LEDS)
