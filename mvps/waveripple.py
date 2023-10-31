import opc
import time
import random
import math

MATRIX_SIZE = 8
STRIP_SIZE = 64
TOTAL_LEDS = MATRIX_SIZE * MATRIX_SIZE + STRIP_SIZE
client = opc.Client('localhost:7890')

# The center of the ripple on the matrix
CENTER_X, CENTER_Y = MATRIX_SIZE // 2, MATRIX_SIZE // 2

def hue_to_rgb(hue):
    r = int(255 * (1 - hue))
    b = int(255 * hue)
    return r, 0, b

def ripple_value(dist, t):
    """Calculate ripple value based on distance and time."""
    value = (1 + math.sin(dist - t)) / 2  # Create a sine wave based on distance
    return value

def main():
    t = 0
    strip_particles = []

    while True:
        pixels = []

        # Generate the matrix ripple
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                dist = math.sqrt((CENTER_X - i)**2 + (CENTER_Y - j)**2)
                brightness = ripple_value(dist, t)

                # Adding some noise
                brightness += random.uniform(-0.1, 0.1)
                brightness = max(0, min(brightness, 1))

                hue = (time.time() * 0.05) % 1  # Slowly shift hue over time
                r, g, b = hue_to_rgb(hue)
                pixels.append((int(r * brightness), int(g * brightness), int(b * brightness)))

        # Handle strip particles
        if random.random() < 0.7:  # Adjusted the chance for faster particle appearance
            hue = random.uniform(0.5, 1)  # Red to blue hue
            strip_particles.append((STRIP_SIZE - 1, hue))  # Start from the top

        # Update and fade existing particles
        new_particles = []
        for pos, hue in strip_particles:
            r, g, b = hue_to_rgb(hue)
            pixels.append((r, g, b))
            if pos > 0:  # Move the particle downwards (reverse direction)
                new_particles.append((pos - 10, hue))  # Decrease position by 10 for much faster movement
        strip_particles = new_particles

        # Fill the rest of the strip
        while len(pixels) < TOTAL_LEDS:
            pixels.append((0, 0, 0))

        client.put_pixels(pixels)
        time.sleep(0.05)
        t += 0.1

if __name__ == "__main__":
    main()
