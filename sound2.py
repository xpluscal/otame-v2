from scipy.io import wavfile
import sounddevice as sd

# Load the WAV file
fs, data = wavfile.read('drone_output.wav')
sd.play(data, fs)
sd.wait()
