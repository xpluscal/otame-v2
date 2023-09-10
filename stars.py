import opc
import time
import colorsys
import random

NUM_LEDS = 64
ADDRESS = 'localhost:7890'
STAR_PROBABILITY = 0.08  
MAX_STAR_BRIGHTNESS = 1.0

class Star:
    def __init__(self):
        self.brightness = 0
        self.direction = 1  # 1 for increasing brightness, -1 for decreasing
        self.speed = random.uniform(0.01, 0.03)  # Random speed for brightness change
        self.max_brightness = random.uniform(0.2, MAX_STAR_BRIGHTNESS)  # Maximum brightness this star can achieve

    def step(self):
        if self.direction == 1 and self.brightness >= self.max_brightness:
            self.direction = -1
        elif self.direction == -1 and self.brightness <= 0:
            self.brightness = 0
            if random.random() < STAR_PROBABILITY:
                self.direction = 1
                self.speed = random.uniform(0.01, 0.03)
                self.max_brightness = random.uniform(0.2, MAX_STAR_BRIGHTNESS)
            return self.brightness
        self.brightness += self.speed * self.direction
        return self.brightness

def main():
    client = opc.Client(ADDRESS)

    if not client.can_connect():
        print('Cannot connect to the server at {0}. Exiting.'.format(ADDRESS))
        return
    
    print('Connected to {0}.'.format(ADDRESS))
    stars = [Star() for _ in range(NUM_LEDS)]
    hue_shift = 0

    try:
        while True:
            pixels = []
            hue_shift = (hue_shift + 0.001) % 1.0  # Slowly shifting hue
            for star in stars:
                star_brightness = star.step()
                
                hue = lerp(0.66, 1.0, hue_shift + star_brightness / 2)  # Introduce a hue shift based on star's brightness
                rgb = colorsys.hsv_to_rgb(hue, 1, star_brightness)
                pixels.append((int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)))
                
            client.put_pixels(pixels)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print('Animation interrupted. Exiting...')
        pixels = [(0, 0, 0)] * NUM_LEDS
        client.put_pixels(pixels)

def lerp(a, b, t):
    return a + t * (b - a)

if __name__ == '__main__':
    main()
