import streamlit as st
from analyse_class import Sound

def main():
    st.title("Slider added frequency plot")
    trial = Sound("trimmed\guitar_tr1_trimmed_ns.wav")

    slider = st.slider("Select Base Frequency", min_value=90.0, max_value=120.0, value=100.0, step=0.1)
    trial.plot_base_freq_slider(slider=slider)


if __name__ == "__main__":
    main()
