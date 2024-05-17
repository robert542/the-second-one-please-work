import streamlit as st
import numpy as np
import scipy.io.wavfile
import sounddevice as sd
import threading

# Define a function to handle sound playing in a thread
def play_sound(sound, sample_rate):
    sd.play(sound, sample_rate)
    sd.wait()

def stop_sound():
    sd.stop()

def synthesize_sound(base_freq, sample_rate, max_harmonic, volume, add_fall_off):
    duration_s = 1  # Shorter duration for interactive playing
    sample_number = np.arange(duration_s * sample_rate)
    total = np.zeros(duration_s * sample_rate)
    for i in range(1, 2 * max_harmonic, 2):
        freq = base_freq * i * np.sqrt(1 + 0.002 * (i ** 2))
        amp = (0.5 / (2 ** i)) * volume if i != 1 else 0.5 * volume
        total += amp * np.sin(2 * np.pi * sample_number * freq / sample_rate)
    
    if add_fall_off:
        decay_shape = np.exp(-sample_number / (1.0 * sample_rate))
        attack_shape = 1 - np.exp(-sample_number / (0.01 * sample_rate))
        total *= decay_shape * attack_shape

    return total

def piano_keyboard(base_freq, sample_rate, max_harmonic, volume, add_fall_off, sound_type):
    # Define piano keys and their frequency multipliers
    keys = ["C", "D", "E", "F", "G", "A", "B", "C'"]
    freqs = [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2]  # Just major scale for simplicity

    for idx, (key, freq_multiplier) in enumerate(zip(keys, freqs)):
        # Append a unique key by using the button label, its index, and sound type
        button_key = f"{key}_{idx}_{sound_type}"  # This makes the key unique per sound type
        if st.button(key, key=button_key):
            freq = base_freq * freq_multiplier
            if sound_type == 'synthesized':
                sound = synthesize_sound(freq, sample_rate, max_harmonic, volume, add_fall_off)
            else:
                sound = modify_uploaded_sound(freq, sample_rate)
            threading.Thread(target=play_sound, args=(sound, sample_rate)).start()



def modify_uploaded_sound(base_freq, sample_rate):
    # This function should modify the pitch of the uploaded sound
    # Placeholder: returning a synthesized sound for demonstration
    return synthesize_sound(base_freq, sample_rate, 3, 1.0, False)

def main():
    st.title('Audio Synthesis App with Piano Interface')
    
    uploaded_file = st.file_uploader("Upload a file", type=["wav"])
    sample_rate = 44100  # Default sample rate
    original_data = None
    if uploaded_file is not None:
        sample_rate, data = scipy.io.wavfile.read(uploaded_file)
        original_data = data.astype(np.float32) / np.iinfo(data.dtype).max  # Normalize audio data

    base_freq = st.slider("Base Frequency", 80.0, 130.0, 100.0, 0.01)
    max_harmonic = st.slider("Max Harmonic (n)", 1, 160, 3)
    volume = st.slider("Volume", 0.1, 2.0, 1.0, 0.1)
    add_fall_off = st.checkbox("Add Fall Off")

    st.write("Piano for Synthesized Sound")
    piano_keyboard(base_freq, sample_rate, max_harmonic, volume, add_fall_off, 'synthesized')

    if original_data is not None:
        st.write("Piano for Uploaded Sound")
        piano_keyboard(base_freq, sample_rate, max_harmonic, volume, add_fall_off, 'uploaded')

    st.button("Stop Sound", on_click=stop_sound)

if __name__ == "__main__":
    main()
