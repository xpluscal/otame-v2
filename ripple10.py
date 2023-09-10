import math
import random
import time
import opc

MATRIX_SIZE = 8
TOTAL_LEDS_MATRIX = MATRIX_SIZE * MATRIX_SIZE
TOTAL_LEDS_STRIP = 64
TOTAL_LEDS = TOTAL_LEDS_MATRIX + TOTAL_LEDS_STRIP
RIPPLE_SPEED = 0.10

def ripple_value(dist, t):
    """Calculate ripple value based on distance and time."""
    frequency = 2.0
    scaled_distance = dist * 2.0
    
    sine_val = math.sin(frequency * (scaled_distance - t * RIPPLE_SPEED))
    window = max(0, 1 - 10 * abs(sine_val))
    
    return window * (1 + sine_val) / 2

def main():
    client = opc.Client('localhost:7890')
    t = 0

    try:
        while True:
            t += 0.05

            # Center smoothly changes over time
            cx = (MATRIX_SIZE - 1) * 0.5 * (math.sin(t * 0.1) + 1)
            cy = (MATRIX_SIZE - 1) * 0.5 * (math.sin(t * 0.15) + 1)

            pixels = []

            # Ripple effect for the matrix
            for i in range(MATRIX_SIZE):
                for j in range(MATRIX_SIZE):
                    dx = i - cx
                    dy = j - cy
                    dist = math.sqrt(dx * dx + dy * dy)

                    intensity = ripple_value(dist, t)

                    # Convert to RGB using the color hue mapping
                    hue = 0.5 + 0.5 * math.sin(t)
                    saturation = 1.0
                    brightness = intensity

                    r, g, b = opc.hue2rgb(hue, saturation, brightness)
                    pixels.append((r, g, b))

            # Transition effect for the strip
            for i in range(TOTAL_LEDS_STRIP):
                hue = 0.5 + 0.5 * math.sin(t + i * 0.1)
                saturation = 1.0
                brightness = max(0, math.sin(t + i * 0.1))
                r, g, b = opc.hue2rgb(hue, saturation, brightness)
                pixels.append((r, g, b))

            client.put_pixels(pixels)
            time.sleep(0.02)

    except KeyboardInterrupt:
        pixels = [(0, 0, 0)] * TOTAL_LEDS
        client.put_pixels(pixels)

if __name__ == "__main__":
    main()
