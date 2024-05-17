import monashspa
import matplotlib.pyplot as plt
import numpy as np
import wave
from matplotlib.widgets import Cursor
from scipy.signal import iirnotch, lfilter

class Sound():

    def __init__(self,filename: str, pre_data=None) -> None:
        if pre_data is None:
            self.filename = filename

            self.signal_wave = wave.open(self.filename, "r")

            #extract the sample rate from the file
            self.sample_rate = self.signal_wave.getframerate()

            #creat numpy array from the waveform
            self.sig = np.frombuffer(self.signal_wave.readframes(-1), dtype=np.int16)
        else:
            self.sig = pre_data[0]
            self.sample_rate = pre_data[1]

        self.fourier = np.fft.rfft(self.sig)
        self.abs_fourier = np.abs(self.fourier)
        self.freq = np.fft.rfftfreq(self.sig.size, d=1./self.sample_rate)

        a=0
        index = -1
        for i in range(len(self.abs_fourier)):
            if self.abs_fourier[i] > a:
                a = self.abs_fourier[i]
                index = i
        print(a)
        print(index)
        print(self.freq[index])
        self.base_freq = self.freq[index]
        self.base_freq_index = index

    def notch_filter(self):
        # Frequencies to remove (50 Hz and its harmonics)
        harmonic_freqs = [50 * i for i in range(1, 25)]  # up to 200 Hz for example
        Q = 30  # Quality factor

        # Sampling frequency
        fs = self.sample_rate  # Adjust as necessary

        filtered_data = self.sig
        for f0 in harmonic_freqs:
            b, a = iirnotch(f0, Q, fs)
            filtered_data = lfilter(b, a, filtered_data)
        return filtered_data

    def plot_waveform(self):
        #create the values for x axis
        sample_numbers = np.arange(len(self.sig))
        #assign variables to be plotted
        #x is the cut of the audio we want to plot
        x = sample_numbers
        # y is the signal strength
        y = self.sig[sample_numbers]

        #plot it
        #create a figure object with an axes ax
        fig, ax = plt.subplots()
        ax.plot(x,y)
        ax.set_xlabel("Sample number")
        ax.set_ylabel("Amplitude")
        ax.set_title("pLoT")

        plt.show()
        #plt.savefig("string_waeform.png")


    def plot_fourier(self, min_lim:int = 0, max_lim:int = 1000):
        fig, ax = plt.subplots()
        ax.plot(self.freq,self.abs_fourier)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Absolute value of FFT")
        ax.set_yscale("log")
        ax.set_title("Fourier transform of recorded waveform")

        ax.set_xlim([min_lim,max_lim])
        value = 50
        while value <= 1000:
            ax.axvline(x=value, color = "green", linestyle="--", linewidth=1)
            value += 50
        cursor = Cursor(ax, color="red", linewidth=1)

        plt.show()
        #plt.savefig("trial1_spectrum.png")

    def plot_base_freq_mult(self):
        fig, ax = plt.subplots()
        ax.plot(self.freq,self.abs_fourier)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Absolute value of FFT")
        ax.set_yscale("log")
        ax.set_title("Fourier transform of Recorded Waveform with Inharmonic fit of Odd Harmonics")
        #add lines
        ax.axvline(x=self.base_freq, color="red", linestyle="--", linewidth=1)
        b=0.002
        value = 3*self.base_freq*np.sqrt(1+9*b)
        n=3
        while value <= 1000:
            ax.axvline(x=value, color = "green", linestyle="--", linewidth=1)
            n+=2
            value = n*self.base_freq*np.sqrt(1+(b*(n**2)))

        ax.set_xlim([0,1000])

        cursor = Cursor(ax, color="red", linewidth=1)

        plt.show()
        #plt.savefig("trial1_spectrum.png")

    def plot_multi_sbs(self):
        pass

    def plot_multi_overlay(self, sound2, sound3 = None, min_lim:int = 0, max_lim:int = 1000):
        fig, ax = plt.subplots()
        ax.plot(self.freq,self.abs_fourier)
        ax.plot(sound2.freq, sound2.abs_fourier, color = "red")
        if type(sound3) != type(None):
            ax.plot(sound3.freq, sound3.abs_fourier, color = "green")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Absolute value of FFT")
        ax.set_yscale("log")
        ax.set_title("Fourier transform of trial 1 with and without 50hz Notch Filter")

        ax.set_xlim([min_lim,max_lim])

        cursor = Cursor(ax, color="red", linewidth=1)
        plt.show()
        #plt.savefig("trials_spectrum.png")


trial = Sound("trimmed\guitar_tr1_trimmed_ns.wav")

# # trial.plot_waveform()
# # trial.plot_fourier()
# trial.plot_base_freq_mult()

# data = trial.notch_filter()
# pre_data = [data, trial.sample_rate]
# filtered = Sound(filename="yeet", pre_data=pre_data )
# filtered.plot_base_freq_mult()

# trial.plot_multi_overlay(filtered)


