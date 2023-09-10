import math
from pydub.generators import Sine


def distance_from_center(x, y, half_matrix):
    dx = x - half_matrix + 0.5
    dy = y - half_matrix + 0.5
    return math.sqrt(dx**2 + dy**2)


def interpolate_color(color1, color2, factor):
    """Interpolate between two RGB colors by a given factor (0-1)."""
    return (
        int(color1[0] + (color2[0] - color1[0]) * factor),
        int(color1[1] + (color2[1] - color1[1]) * factor),
        int(color1[2] + (color2[2] - color1[2]) * factor)
    )


def hue_to_pitch(hue):
    """
    Map hue value (0-1) to a pitch (frequency in Hz).
    For simplicity, we are mapping it linearly here. You can replace this with a more complex mapping if desired.
    """
    MIN_PITCH = 200  # Adjust as per your requirements
    MAX_PITCH = 800  # Adjust as per your requirements
    return MIN_PITCH + hue * (MAX_PITCH - MIN_PITCH)


def generate_sound_for_color(hue, saturation, brightness):
    """Generate a sound sample based on the given color attributes."""

    # Map the hue to a frequency between 200Hz and 600Hz
    freq = 200 + hue * 400

    # Map the saturation to amplitude between 0.5 and 1.0
    amplitude = 0.5 + saturation * 0.5

    # Limit amplitude between 0 and 1
    amplitude = max(0, min(amplitude, 1))

    # Duration in milliseconds based on brightness
    duration_ms = 500 + brightness * 500

    sine_wave = Sine(freq)

    audio_sample = sine_wave.to_audio_segment(
        duration=5000,
        volume=-10.0
    )

    return audio_sample
