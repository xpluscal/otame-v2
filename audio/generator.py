import numpy as np

class AudioGenerator:
    def generate_drone(self, frequency, duration, volume=0.5):
        # Using numpy to generate a continuous sine wave
        t = np.linspace(0, duration, int(duration * 44100), False)
        drone = np.sin(frequency * t * 2 * np.pi)
        # Normalize to 16-bit range and adjust volume
        drone = (drone * volume * (2**15 - 1) /
                 np.max(np.abs(drone))).astype(np.int16)
        return drone

    def generate_pulse(self, frequency, rate, duration):
        # LFO to modulate the amplitude for pulsing effect
        t = np.linspace(0, duration, int(duration * 44100), False)
        lfo = 0.5 * np.sin(rate * t * 2 * np.pi) + \
            0.5  # Oscillate between 0 and 1
        pulse = np.sin(frequency * t * 2 * np.pi)
        pulse = (pulse * lfo * (2**15 - 1) /
                 np.max(np.abs(pulse))).astype(np.int16)
        return pulse

    def generate_high_tinkle(self, frequency, duration, random_variation=0.1):
        t = np.linspace(0, duration, int(duration * 44100), False)
        # Introducing random frequency variation for 'tinkle' effect
        frequency_variation = frequency + \
            (np.random.rand() - 0.5) * 2 * random_variation * frequency
        tinkle = np.sin(frequency_variation * t * 2 * np.pi)
        tinkle = (tinkle * (2**15 - 1) /
                  np.max(np.abs(tinkle))).astype(np.int16)
        return tinkle
