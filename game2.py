import opc
import time
import random

MATRIX_SIZE = 8
STRIP_SIZE = 64
TOTAL_LEDS = MATRIX_SIZE * MATRIX_SIZE + STRIP_SIZE
client = opc.Client('localhost:7890')

def rule30(left, center, right):
    return left ^ (center or right)

def step_1d(row):
    new_row = []
    for i in range(len(row)):
        left = row[i-1]
        center = row[i]
        right = row[(i+1) % len(row)]
        new_row.append(rule30(left, center, right))
    return new_row

def hue_to_rgb(hue):
    # Convert a hue (0-1) into an RGB value
    # We'll use a simple gradient from red to blue
    r = int(255 * (1 - hue))
    b = int(255 * hue)
    return r, 0, b

def main():
    # Initialize with one live cell in the center
    row = [0] * (MATRIX_SIZE // 2 - 1) + [1] + [0] * (MATRIX_SIZE // 2 - 1)
    generations = [row]

    while True:
        # Convert to color
        pixels = []
        hue = (time.time() * 0.05) % 1  # Slowly shift hue over time
        
        for gen_index, gen in enumerate(generations):
            for cell in gen:
                brightness = 1 - (gen_index / (MATRIX_SIZE + STRIP_SIZE))
                r, g, b = hue_to_rgb(hue)
                color = (int(r * brightness * cell), int(g * brightness * cell), int(b * brightness * cell))
                pixels.append(color)

        # Fill in any remaining LEDs with off (0, 0, 0)
        pixels.extend([(0, 0, 0)] * (TOTAL_LEDS - len(pixels)))
        
        # Send to matrix + strip
        client.put_pixels(pixels)
        time.sleep(0.2)

        # Step the automaton
        new_row = step_1d(generations[-1])
        generations.append(new_row)
        if len(generations) > MATRIX_SIZE + STRIP_SIZE:
            generations.pop(0)

if __name__ == "__main__":
    main()
