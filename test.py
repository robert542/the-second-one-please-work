import numpy as np
import wave

import numpy as np
import wave
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

class Sound:
    def __init__(self, uploaded_file, fft_points=None) -> None:
        self.uploaded_file = uploaded_file
        self.signal_wave = wave.open(self.uploaded_file, "r")
        self.sample_rate = self.signal_wave.getframerate()
        self.sig = np.frombuffer(self.signal_wave.readframes(-1), dtype=np.int16)

        # Set the number of FFT points, using zero-padding if specified
        if fft_points is None:
            self.fft_points = len(self.sig)
        else:
            self.fft_points = fft_points  # Zero-padding if this is larger than len(self.sig)

        self.fourier = np.fft.rfft(self.sig, n=self.fft_points)
        self.abs_fourier = np.abs(self.fourier)
        self.freq = np.fft.rfftfreq(self.fft_points, d=1./self.sample_rate)

        # Calculate the base frequency
        self.base_freq = self.freq[np.argmax(self.abs_fourier)]
        self.base_freq_index = np.argmax(self.abs_fourier)

    def plot_fourier(self, min_lim=0, max_lim=5000):
        fig, ax = plt.subplots()
        ax.plot(self.freq, self.abs_fourier)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Absolute value of FFT")
        ax.set_yscale("log")
        ax.set_title("Fourier Transform of Recorded Waveform")
        ax.set_xlim([min_lim, max_lim])

        # Plot vertical lines at the base frequency and its odd integer multiples
        for i in range(1, 11, 2):  # Adjust range as needed
            multiple = self.base_freq * i
            if multiple > max_lim:
                break
            ax.axvline(x=multiple, color="red", linestyle="--", label=f'{i}x Base Freq' if i == 1 else '')

        cursor = Cursor(ax, color="red", linewidth=1)
        plt.legend()
        plt.show()

# Example usage
trial = Sound("trimmed\guitar_tr1_trimmed_ns.wav", fft_points=2**18)  # You can change 4096 to another power of two depending on desired resolution
trial.plot_fourier(min_lim=0, max_lim=1000)
