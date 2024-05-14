import streamlit as st
from analyse_class import Sound
import numpy as np

def main():
    st.title("Interactive Fourier Transform Plot")


    # Initialize Sound object
    sound = Sound("trimmed\guitar_tr1_trimmed_ns.wav")

    # Slider for base frequency
    base_freq = st.slider('Base Frequency', min_value=90.0, max_value=140.0, value=100.0, step=0.1)

    # Get figure from Sound object and plot it
    fig = sound.plot_base_freq_slider_web(base_freq)
    st.pyplot(fig)

if __name__ == "__main__":
    main()
