import opc
import time
import colorsys
import random

NUM_LEDS = 128
ADDRESS = 'localhost:7890'
CHASE_SIZE_MIN = 3
CHASE_SIZE_MAX = 8
FADE_FACTOR = 0.8

def lerp(a, b, t):
    return a + t * (b - a)

def chase_effect(position, chase_size, direction):
    pixels = [(0, 0, 0)] * NUM_LEDS
    for i in range(chase_size):
        idx = (position + i * direction) % NUM_LEDS
        hue = lerp(0.66, 1.0, (i / chase_size))  # Interpolate between blue and red
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        pixels[idx] = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
    
    # Fade previous state
    for i in range(NUM_LEDS):
        r, g, b = pixels[i]
        pixels[i] = (int(r * FADE_FACTOR), int(g * FADE_FACTOR), int(b * FADE_FACTOR))
    return pixels

def main():
    client = opc.Client(ADDRESS)

    if not client.can_connect():
        print('Cannot connect to the server at {0}. Exiting.'.format(ADDRESS))
        return
    
    print('Connected to {0}.'.format(ADDRESS))
    position = 0
    previous_pixels = [(0, 0, 0)] * NUM_LEDS
    chase_size = random.randint(CHASE_SIZE_MIN, CHASE_SIZE_MAX)
    direction = 1 if random.random() < 0.5 else -1

    try:
        while True:
            pixels = chase_effect(position, chase_size, direction)
            
            # Blend new pixels with faded previous state
            blended_pixels = [
                (int(p[0] + previous_pixels[i][0]), int(p[1] + previous_pixels[i][1]), int(p[2] + previous_pixels[i][2]))
                for i, p in enumerate(pixels)
            ]
            client.put_pixels(blended_pixels)
            previous_pixels = blended_pixels
            
            time.sleep(0.05 + random.uniform(0, 0.1))  # Randomized delay
            position += direction
            if position >= NUM_LEDS or position < 0:
                position = 0 if direction == 1 else NUM_LEDS - 1
                time.sleep(0.5 + random.uniform(0, 1))  # Random pause between chases
                chase_size = random.randint(CHASE_SIZE_MIN, CHASE_SIZE_MAX)
                direction = 1 if random.random() < 0.5 else -1
    except KeyboardInterrupt:
        print('Animation interrupted. Exiting...')
        pixels = [(0, 0, 0)] * NUM_LEDS
        client.put_pixels(pixels)

if __name__ == '__main__':
    main()
