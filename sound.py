import numpy as np
import sounddevice as sd

# Generate a 440Hz test tone for 1 second
fs = 44100  # Sample rate
duration = 1  # seconds
frequency = 440  # Hz
t = np.linspace(0, duration, int(fs * duration), endpoint=False)  # Time array
test_tone = np.sin(2 * np.pi * frequency * t)

sd.play(test_tone, samplerate=fs)
sd.wait()
