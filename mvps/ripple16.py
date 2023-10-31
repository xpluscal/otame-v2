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

# Create a client object
client = opc.Client('localhost:7890')

# Function to calculate distance from the center of a matrix
def distance_from_center(x, y):
    dx = x - HALF_MATRIX + 0.5
    dy = y - HALF_MATRIX + 0.5
    return math.sqrt(dx**2 + dy**2)

def calculate_rgb_from_hsb(h, s, b):
    """Calculate RGB from HSB."""
    h = h % 360
    chroma = b * s
    x = chroma * (1 - abs(((h / 60) % 2) - 1))
    m = b - chroma

    if 0 <= h < 60:
        r, g, b = chroma, x, 0
    elif 60 <= h < 120:
        r, g, b = x, chroma, 0
    elif 120 <= h < 180:
        r, g, b = 0, chroma, x
    elif 180 <= h < 240:
        r, g, b = 0, x, chroma
    elif 240 <= h < 300:
        r, g, b = x, 0, chroma
    else:
        r, g, b = chroma, 0, x

    r, g, b = (r + m) * 255, (g + m) * 255, (b + m) * 255
    return int(r), int(g), int(b)

def get_color_for_shift(shift):
    """Determine the color based on the shift value."""
    hue = 360 * shift  # Shift smoothly between 0 (red) to 360 (again red but we stop at blue)
    saturation = 1  # full saturation
    brightness = 1  # will be adjusted by the ripple effect

    return calculate_rgb_from_hsb(hue, saturation, brightness)

try:
    # Main animation loop
    while True:
        pixels = []
        t = time.time() * SPEED_FACTOR

        for matrix_num in range(TOTAL_MATRICES):
            matrix_offset_x = (matrix_num % 2) * MATRIX_SIZE
            matrix_offset_y = (matrix_num // 2) * MATRIX_SIZE

            for y in range(MATRIX_SIZE):
                for x in range(MATRIX_SIZE):
                    adjusted_x = x + matrix_offset_x
                    adjusted_y = y + matrix_offset_y
                    
                    distance = distance_from_center(adjusted_x % 8, adjusted_y % 8)
                    
                    brightness = (math.sin(t - distance) + 1) / 2  # produces values between 0 and 1
                    led_color_shift = (math.sin(t) + 1) / 2  # Shift between 0 and 1

                    r, g, b = get_color_for_shift(led_color_shift)
                    r = int(r * brightness)
                    g = int(g * brightness)
                    b = int(b * brightness)

                    pixels.append((r, g, b))

        # Send pixels to Fadecandy
        client.put_pixels(pixels)

        # Wait for a short period of time before the next frame
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Interrupted by user. Exiting...")
    # Turn off all LEDs
    client.put_pixels([(0, 0, 0)] * TOTAL_LEDS)
