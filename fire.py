import opc
import time
import math
import random

# Configuration
TOTAL_LEDS = 64
SPEED_FACTOR = 1.75
COLOR_CHANGE_SPEED = 0.5
NOISE_FACTOR = 0.2

# Create a client object
client = opc.Client('localhost:7890')

# Fire color palette
colors = [
    (255, 0, 0),       # Red
    (255, 85, 0),      # Orange-red
    (255, 170, 0),     # Dark yellow
    (255, 255, 85)     # Yellow
]


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

        t = time.time()
        color_shift = (math.sin(t * COLOR_CHANGE_SPEED) + 1) / 2

        for i in range(TOTAL_LEDS):
            # Map LED index to a "fire height" (from bottom to top)
            heat = int((TOTAL_LEDS - i) / TOTAL_LEDS * len(colors))
            flame_intensity = random.randint(0, heat)
            base_color = colors[flame_intensity]

            noise_r = random.randint(-int(NOISE_FACTOR*255),
                                     int(NOISE_FACTOR*255))
            noise_g = random.randint(-int(NOISE_FACTOR*255),
                                     int(NOISE_FACTOR*255))
            noise_b = random.randint(-int(NOISE_FACTOR*255),
                                     int(NOISE_FACTOR*255))

            r = min(255, max(0, base_color[0] + noise_r))
            g = min(255, max(0, base_color[1] + noise_g))
            b = min(255, max(0, base_color[2] + noise_b))

            brightness = (math.sin(t * SPEED_FACTOR - i) + 1) / 2
            pixels.append(
                (int(r*brightness), int(g*brightness), int(b*brightness)))

        # Send pixels to Fadecandy
        client.put_pixels(pixels)
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Interrupted by user. Exiting...")
    # Turn off all LEDs
    client.put_pixels([(0, 0, 0)] * TOTAL_LEDS)
