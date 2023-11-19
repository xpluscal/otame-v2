import random
from sc3.all import *
import time
import math

from sc3.all import *

# Set server options
s.options.sample_rate = 44100  # Or the sample rate you verified works
s.options.num_input_bus_channels = 0  # Disable input channels if not used

# Boot the server
s.boot()

# Add a delay to ensure server is fully booted
time.sleep(3)

# ... rest of your script ...

angle = 0  # Initialize angle
angle_increment = math.pi / 200  # Adjust for speed of movement

next_movement_time = 0
last_time = time.time()

counter = 0
drone_update_interval = 100  # Adjust this for the drone's slower update rate
bass_drone_update_interval = 4000  # Adjust this for the bass drone's slower update rate
underwater_movement_update_interval = 4000  # Adjust this for the underwater movement's slower update rate


@synthdef
def sine(freq=440, amp=0.1, gate=1):
    sig = SinOsc(freq) * amp
    env = EnvGen(Env.adsr(), gate, done_action=2)
    Out(0, (sig * env).dup())

@synthdef
def bubble_synth(pan=0, amp=0.001, dur=0.1):
    # Noise generator
    noise = WhiteNoise.ar()

    # Use a band-pass filter to get a 'bubble' sound
    bubble = BPF.ar(noise, freq=800, rq=0.1) * amp  # Use 'amp' here

    # Envelope to control the duration and shape of the bubble sound
    env = EnvGen.ar(Env.perc(0.01, dur), done_action=2)

    # Apply the envelope to the bubble sound
    bubbly_sound = bubble * env

    # Pan the sound across the stereo field
    panned_sound = Pan2.ar(bubbly_sound, pan)

    Out.ar(0, panned_sound)


bubble_synth.send()

@synthdef
def reverb_effect(bus, room_size=0.8, mix=0.3):
    # Get the audio signal from the specified bus
    input_signal = In.ar(bus, 2)  # Assuming stereo signal

    # Apply reverb
    wet_signal = FreeVerb.ar(input_signal, room_size, mix, damp=0.4)

    Out.ar(0, wet_signal)


reverb_effect.send()

@synthdef
def underwater_movement(pan=0, amp=0.3, rate=1, room_size=0.8, mix=0.3):
    # White noise generator
    noise = WhiteNoise.ar()

    # Filter the noise to simulate underwater quality
    filtered_noise = LPF.ar(noise, freq=300)  # Low pass filter for a muffled sound

    # Modulate the filter frequency to simulate movement
    lfo = SinOsc.kr(rate).range(200, 400)  # Change in frequency
    modulated_noise = LPF.ar(filtered_noise, freq=lfo)

    # Pan the sound for spatial movement
    panned_noise = Pan2.ar(modulated_noise, pan)

    # Apply amplitude
    output = panned_noise * amp

    # Apply reverb directly to the output signal
    wet_signal = FreeVerb.ar(output, room_size, mix, damp=0.4)

    # Output the reverberated sound
    Out.ar(0, wet_signal.dup())

underwater_movement.send()

@synthdef
def bass_drone_synth(freq=55, amp=0.2, lfo_rate=0.2, lfo_depth=0.1):
    # Layer multiple oscillators for a fuller sound
    osc1 = Saw.ar(freq) * amp
    osc2 = Saw.ar(freq * 0.5) * (amp * 0.8)  # An octave lower
    osc3 = Saw.ar(freq * 2) * (amp * 0.5)  # An octave higher

    combined_osc = osc1 + osc2 + osc3

    # Low-pass filter to emphasize bass frequencies
    filtered_wave = LPF.ar(combined_osc, freq=120)

    # LFO for the pulsing effect
    lfo = SinOsc.kr(lfo_rate) * lfo_depth * amp + amp

    # Apply LFO to amplitude for pulsing
    pulsing_wave = filtered_wave * lfo
    

    # Optional: Add subtle distortion for warmth
    distorted_wave = pulsing_wave.clip2(0.6)  # Adjust the clipping level as needed

    # Output the sound
    Out.ar(0, distorted_wave.dup())


# @synthdef
# def bass_drone_synth(freq=55, amp=0.2, lfo_rate=0.2, lfo_depth=0.1):
#     # Sawtooth wave for a harsher, industrial tone
#     raw_wave = Saw.ar(freq) * amp

#     # LFO for the pulsing effect
#     lfo = SinOsc.kr(lfo_rate) * lfo_depth + 1

#     # Apply LFO to amplitude for pulsing
#     pulsing_wave = raw_wave * lfo

#     # Output the sound
#     Out.ar(0, pulsing_wave.dup())

bass_drone_synth.send()

@synthdef
def drone_synth(base_freq=100, amp=0.3, mod_rate=0.2, mod_depth=0.1):
    # Create two oscillators slightly detuned for a fuller sound
    osc1 = SinOsc(base_freq) * amp
    osc2 = SinOsc(base_freq * 1.005) * amp  # slightly detuned

    # Modulation for a rolling effect
    lfo = SinOsc(mod_rate) * mod_depth + 1

    # Apply modulation to the amplitude
    sig = (osc1 + osc2) * lfo

    # Stereo output
    Out(0, sig.dup())

drone_synth.send()

time.sleep(2)  # Short delay to ensure the SynthDef is registered

drone = Synth('drone_synth', {'base_freq': 400, 'amp': 0.1, 'mod_rate': 0.1, 'mod_depth': 0.05})
drone2 = Synth('drone_synth', {'base_freq': 200, 'amp': 0.1, 'mod_rate': 0.1, 'mod_depth': 0.05})
drone3 = Synth('drone_synth', {'base_freq': 100, 'amp': 0.1, 'mod_rate': 0.1, 'mod_depth': 0.05})
bass_drone = Synth('bass_drone_synth', {'freq': 55, 'amp': 0.3, 'lfo_rate': 0.22, 'lfo_depth': 0.8})

try:
    while True:

        current_time = time.time()

        if counter % drone_update_interval == 0:
            mod_rate = random.uniform(0.05, 0.2)
            mod_depth = random.uniform(0.05, 0.15)
            drone.set('mod_rate', mod_rate)
            drone.set('mod_depth', mod_depth)

            drone2.set('mod_rate', mod_rate)
            drone2.set('mod_depth', mod_depth)

            drone3.set('mod_rate', mod_rate)
            drone3.set('mod_depth', mod_depth)

        if counter % bass_drone_update_interval == 0:
            # Optionally, adjust parameters over time for variation
            lfo_rate_val = random.uniform(0.05, 0.2)
            lfo_depth_val = random.uniform(0.3, 0.7)

            bass_drone.set('lfo_rate', lfo_rate_val)
            bass_drone.set('lfo_depth', lfo_depth_val)

        # Handle intermittent underwater movement
        if current_time >= next_movement_time:
            # Random pan value and rate for the next movement
            pan_val = random.uniform(-1, 1)
            rate_val = random.uniform(0.1, 0.5)

            # Create or update the underwater movement sound
            if 'movement' in locals():
                movement.free()  # Free the existing movement before creating a new one

            movement = Synth('underwater_movement', {'pan': pan_val, 'amp': 0.4, 'rate': rate_val})
            
            # Calculate next movement time
            next_movement_duration = random.uniform(2, 3)  # Duration of movement sound
            next_wait_duration = random.uniform(6, 10)  # Duration of silence
            next_movement_time = current_time + next_movement_duration + next_wait_duration

        # Increment the counter
        counter += 1

        pan_val = math.cos(angle)  # Range from -1 to 1
        dur_val = (math.sin(angle) + 1) / 2  # Normalize range from 0 to 1

        # Create a bubble sound with moving stereo position and varying volume
        # Example of creating a bubble sound with a specific amplitude
        bubble = Synth('bubble_synth', {'pan': pan_val, 'amp': 0.01, 'dur': dur_val})


        # Increment the angle for the next iteration
        angle += angle_increment
        if angle >= 2 * math.pi:
            angle -= 2 * math.pi  # Reset angle after a full 
            
        loop_duration = time.time() - last_time
        time_to_sleep = max(0.01, 0.1 - loop_duration)
        time.sleep(time_to_sleep)
        last_time = time.time()


        # Wait before the next loop iteration
        # time.sleep(random.uniform(0.01, 0.1))  # Adjust for desired bubble frequency
except KeyboardInterrupt:
    # Stop the synth and exit
    drone.free()
    drone2.free()
    drone3.free()
    bass_drone.free()
    bubble.free()
    movement.free()
    reverb.free()
    s.quit()