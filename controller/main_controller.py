from audio.generator import AudioGenerator
from utils.helpers import play_sound
from scipy.io.wavfile import write
import numpy as np

class MainController:
    def __init__(self):
        self.gen = AudioGenerator()

    def play_alien_sounds(self):
        drone = self.gen.generate_drone(120, 10)
        pulse = self.gen.generate_pulse(500, 2, 10)
        tinkle = self.gen.generate_high_tinkle(500, 10)

        print("Drone: ", drone)
        print("Pulse: ", pulse)
        print("Tinkle: ", tinkle)

        write("drone_output.wav", 44100, drone)
        write("pulse_output.wav", 44100, pulse)
        write("tinkle_output.wav", 44100, tinkle)

        combined_sound = drone + pulse + tinkle
        normalized_sound = (combined_sound * (2**15 - 1) /
                            np.max(np.abs(combined_sound))).astype(np.int16)

        play_sound(normalized_sound)

    def main_loop(self):
        while True:
            # In future, this loop will handle other things like visual updates, user interactions, etc.
            # For now, it will just play the sounds.
            self.play_alien_sounds()


if __name__ == "__main__":
    controller = MainController()
    controller.main_loop()
