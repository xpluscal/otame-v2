import sounddevice as sd

desired_device_name = "UE MEGABOOM"
device_info = sd.query_devices()

for idx, device in enumerate(device_info):
    if device['name'] == desired_device_name:
        sd.default.device = idx
        sd.default.channels = 1  # Set default channels to 1 (mono)
        break


def play_sound(sound_array):
    sd.play(sound_array, samplerate=44100, channels=1)
    sd.wait()
