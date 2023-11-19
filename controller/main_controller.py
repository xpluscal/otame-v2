from audio.generator import AudioGenerator
from utils.helpers import play_sound
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plt

class MainController:
    def __init__(self):
        self.gen = AudioGenerator()

    def play_alien_sounds(self):
        drone = self.gen.generate_drone(120, 10)
        pulse = self.gen.generate_pulse(500, 2, 10)
        tinkle = self.gen.generate_high_tinkle(500, 10)

        # Ensure all arrays are the same length for combining
        max_length = max(len(drone), len(pulse), len(tinkle))
        
        # Pad shorter arrays with zeros to match the maximum length
        drone = np.pad(drone, (0, max_length - len(drone)), 'constant')
        pulse = np.pad(pulse, (0, max_length - len(pulse)), 'constant')
        tinkle = np.pad(tinkle, (0, max_length - len(tinkle)), 'constant')

        print("Lengths after padding:")
        print("Drone: ", len(drone))
        print("Pulse: ", len(pulse))
        print("Tinkle: ", len(tinkle))

        # Save the individual sounds to verify they are not silent
        write("drone_output.wav", 44100, drone)
        write("pulse_output.wav", 44100, pulse)
        write("tinkle_output.wav", 44100, tinkle)

        # Combine the sounds
        combined_sound = drone + pulse + tinkle

        # Check the stats of the combined sound
        print("Combined sound stats:")
        print("Max value:", np.max(combined_sound))
        print("Min value:", np.min(combined_sound))
        print("Mean value:", np.mean(combined_sound))

        # Normalization with headroom to avoid clipping
        headroom = 0.8
        max_combined_amplitude = np.max(np.abs(combined_sound)) * headroom
        normalized_sound = (combined_sound * (2**15 - 1) / max_combined_amplitude).astype(np.int16)

        # Check the stats of the normalized sound
        print("Normalized sound stats:")
        print("Max value:", np.max(normalized_sound))
        print("Min value:", np.min(normalized_sound))
        print("Mean value:", np.mean(normalized_sound))

        # Play the normalized sound
        play_sound(normalized_sound)

        # Also write the combined sound to a file to check with an external player
        write("combined_output.wav", 44100, normalized_sound)



    def main_loop(self):
        while True:
            # In future, this loop will handle other things like visual updates, user interactions, etc.
            # For now, it will just play the sounds.
            self.play_alien_sounds()


if __name__ == "__main__":
    controller = MainController()
    controller.main_loop()
