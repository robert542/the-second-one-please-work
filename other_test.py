import streamlit as st
import numpy as np
import sounddevice as sd

def synthesize_sound(frequencies, amplitudes, sample_rate, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = np.zeros_like(t)
    for freq, amp in zip(frequencies, amplitudes):
        waveform += amp * np.sin(2 * np.pi * freq * t)
    return waveform

def play_sound(sound, sample_rate):
    sd.play(sound, sample_rate)
    sd.wait()

def main():
    st.title("Waveform Synthesis App")

    with st.form("waveform_input"):
        num_waves = st.number_input("Number of waves", min_value=1, max_value=10, value=1)
        frequencies = []
        amplitudes = []

        for i in range(num_waves):
            freq = st.number_input(f"Frequency {i+1}", value=440.0, format="%.2f")
            amp = st.number_input(f"Amplitude {i+1}", value=1.0, min_value=0.0, max_value=1.0, step=0.1)
            frequencies.append(freq)
            amplitudes.append(amp)

        sample_rate = st.selectbox("Sample Rate", options=[44100, 48000, 32000], index=0)
        duration = st.slider("Duration of the sound (seconds)", min_value=1, max_value=10, value=2)
        submit_button = st.form_submit_button("Generate and Play Sound")

    if submit_button:
        sound = synthesize_sound(frequencies, amplitudes, sample_rate, duration)
        play_sound(sound, sample_rate)

if __name__ == "__main__":
    main()
