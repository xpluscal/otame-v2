import pygame
import opc
import time
import math
import random
from pydub.playback import play
from led_audio_utils import distance_from_center, interpolate_color, generate_sound_for_color

# Configuration
MATRIX_SIZE = 8
HALF_MATRIX = MATRIX_SIZE // 2
TOTAL_MATRICES = 4
LEDS_PER_MATRIX = 64
TOTAL_LEDS = LEDS_PER_MATRIX * TOTAL_MATRICES
SPEED_FACTOR = 1.75  # Increases the speed of the animation
COLOR_CHANGE_SPEED = 0.5  # Controls the speed of color change
NOISE_FACTOR = 0.2  # Intensity of the noise for color variation

# Create a client object
client = opc.Client('localhost:7890')


def custom_play(audio_segment):
    pygame.mixer.init(frequency=audio_segment.frame_rate)
    pygame.mixer.music.load(audio_segment.export(format="wav").read())
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()

try:
    # Main animation loop
    while True:
        pixels = []

        # Get the current time to use as an animation factor
        t = time.time()

        color_shift = (math.sin(t * COLOR_CHANGE_SPEED) + 1) / \
            2  # produces values between 0 and 1

        # Loop over matrices
        for matrix_num in range(TOTAL_MATRICES):
            matrix_offset_x = (matrix_num % 2) * MATRIX_SIZE
            matrix_offset_y = (matrix_num // 2) * MATRIX_SIZE
            for y in range(MATRIX_SIZE):
                for x in range(MATRIX_SIZE):
                    adjusted_x = x + matrix_offset_x
                    adjusted_y = y + matrix_offset_y

                    distance = distance_from_center(
                        adjusted_x % 8, adjusted_y % 8, HALF_MATRIX)

                    # Adjusted brightness formula
                    brightness = (
                        math.sin(t * SPEED_FACTOR - distance) + 1) / 2

                    # Direct RGB interpolation between Red and Blue
                    base_color = interpolate_color(
                        (255, 0, 0), (0, 0, 255), color_shift)

                    noise_r = random.randint(-int(NOISE_FACTOR*255),
                                             int(NOISE_FACTOR*255))
                    noise_g = random.randint(-int(NOISE_FACTOR*255),
                                             int(NOISE_FACTOR*255))
                    noise_b = random.randint(-int(NOISE_FACTOR*255),
                                             int(NOISE_FACTOR*255))

                    r = min(255, max(0, base_color[0] + noise_r))
                    g = min(255, max(0, base_color[1] + noise_g))
                    b = min(255, max(0, base_color[2] + noise_b))

                    pixels.append(
                        (int(r*brightness), int(g*brightness), int(b*brightness)))

        # Play sound corresponding to the primary color of the animation
        hue = color_shift
        saturation = 1  # Full saturation for now
        audio_sample = generate_sound_for_color(hue, saturation, brightness)
        custom_play(audio_sample)

        # Send pixels to Fadecandy
        client.put_pixels(pixels)

        # Wait for a short period of time before the next frame
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Interrupted by user. Exiting...")
    # Turn off all LEDs
    client.put_pixels([(0, 0, 0)] * TOTAL_LEDS)
