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
SPEED_FACTOR = 2.0  # Increases the speed of the animation
COLOR_CHANGE_SPEED = 0.5  # Controls the speed of color change
NOISE_FACTOR = 0.1  # Intensity of the noise for color variation

# Create a client object
client = opc.Client('localhost:7890')

# Function to calculate distance from the center of a matrix
def distance_from_center(x, y):
    dx = x - HALF_MATRIX + 0.5
    dy = y - HALF_MATRIX + 0.5
    return math.sqrt(dx**2 + dy**2)

def interpolate_color(color1, color2, factor):
    """Interpolate between two RGB colors by a given factor (0-1)."""
    return (
        int(color1[0] + (color2[0] - color1[0]) * factor),
        int(color1[1] + (color2[1] - color1[1]) * factor),
        int(color1[2] + (color2[2] - color1[2]) * factor)
    )

try:
    # Main animation loop
    while True:
        pixels = []

        # Get the current time to use as an animation factor
        t = time.time() * SPEED_FACTOR

        # Breathing effect (synchronized with color change)
        wave_factor = math.sin(t * COLOR_CHANGE_SPEED)

        # Calculate the color shift
        color_shift = (wave_factor + 1) / 2  # produces values between 0 and 1

        # Loop over matrices
        for matrix_num in range(TOTAL_MATRICES):
            matrix_offset_x = (matrix_num % 2) * MATRIX_SIZE
            matrix_offset_y = (matrix_num // 2) * MATRIX_SIZE

            for y in range(MATRIX_SIZE):
                for x in range(MATRIX_SIZE):
                    adjusted_x = x + matrix_offset_x
                    adjusted_y = y + matrix_offset_y

                    distance = distance_from_center(adjusted_x % 8, adjusted_y % 8)

                    # Modify the brightness formula to take the wave_factor into account
                    brightness = (math.sin(t - distance * (wave_factor + 1.5)) + 1) / 2

                    # Direct RGB interpolation between Red and Blue
                    base_color = interpolate_color((255, 0, 0), (0, 0, 255), color_shift)
                    
                    noise_r = random.randint(-int(NOISE_FACTOR*255), int(NOISE_FACTOR*255))
                    noise_g = random.randint(-int(NOISE_FACTOR*255), int(NOISE_FACTOR*255))
                    noise_b = random.randint(-int(NOISE_FACTOR*255), int(NOISE_FACTOR*255))

                    r = min(255, max(0, base_color[0] + noise_r))
                    g = min(255, max(0, base_color[1] + noise_g))
                    b = min(255, max(0, base_color[2] + noise_b))

                    pixels.append((int(r*brightness), int(g*brightness), int(b*brightness)))

        # Send pixels to Fadecandy
        client.put_pixels(pixels)

        # Wait for a short period of time before the next frame
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Interrupted by user. Exiting...")
    # Turn off all LEDs
    client.put_pixels([(0, 0, 0)] * TOTAL_LEDS)
