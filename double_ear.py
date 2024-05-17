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
    duration_s = 8
    sample_number = np.arange(duration_s * sample_rate)
    total = np.zeros(duration_s * sample_rate)
    for i in range(1, 2 * max_harmonic, 2):  # Generating odd multiples up to the 2n-1 harmonic
        b=0.002
        freq = base_freq * i * np.sqrt(1+(b*(i**2)))
        if i != 1:
            amp = (0.5 / (2**i)) * volume  # More intense drop-off for harmonics
        else:
            amp = 0.5 * volume  # Full volume for the fundamental frequency
        phase = 0  # No phase shift
        total += amp * np.sin(2 * np.pi * sample_number * freq / sample_rate + phase)
    
    if add_fall_off:
        decay_shape = np.exp(-sample_number / (1.0 * sample_rate))
        attack_shape = 1 - np.exp(-sample_number / (0.01 * sample_rate))
        total *= decay_shape * attack_shape

    return total

def main():
    st.title('Audio Synthesis App')
    
    uploaded_file = st.file_uploader("Upload a file", type=["wav"])
    sample_rate = 44100  # Default sample rate
    original_data = None
    if uploaded_file is not None:
        sample_rate, data = scipy.io.wavfile.read(uploaded_file)
        original_data = data.astype(np.float32) / np.iinfo(data.dtype).max  # Normalize audio data
        st.write(f"Sample rate: {sample_rate}")
        volume = st.slider("Volume for original sound", 0.1, 2.0, 1.0, 0.1)
        original_data *= volume
        if st.button('Play Original Sound'):
            threading.Thread(target=play_sound, args=(original_data, sample_rate)).start()

    base_freq = st.slider("Base Frequency", 80.0, 130.0, 100.0, 0.01)
    max_harmonic = st.slider("Max Harmonic (n)", 1, 160, 3)
    volume = st.slider("Volume for synthesized sound", 0.1, 2.0, 1.0, 0.1)
    add_fall_off = st.checkbox("Add Fall Off")

    synthesized_sound = synthesize_sound(base_freq, sample_rate, max_harmonic, volume, add_fall_off)
    synthesized_sound = synthesized_sound.astype(np.float32)  # Ensure proper data type

    if st.button('Play Synthesized Sound'):
        threading.Thread(target=play_sound, args=(synthesized_sound, sample_rate)).start()

    # Play both sounds in stereo
    if original_data is not None and st.button("Play Both Sounds"):
        # Pad the shorter sound with zeros if necessary
        min_length = min(len(original_data), len(synthesized_sound))
        stereo_sound = np.zeros((min_length, 2), dtype=np.float32)
        stereo_sound[:, 0] = original_data[:min_length]  # Left channel
        stereo_sound[:, 1] = synthesized_sound[:min_length]  # Right channel
        threading.Thread(target=play_sound, args=(stereo_sound, sample_rate)).start()

    st.button("Stop Sound", on_click=stop_sound)

if __name__ == "__main__":
    main()
