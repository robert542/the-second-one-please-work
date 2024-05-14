import matplotlib.pyplot as plt
import numpy as np
import wave
from matplotlib.widgets import Cursor, Slider
import streamlit as st



class Sound():

    def __init__(self, uploaded_file) -> None:
        #self.filename = filename
        self.uploaded_file = uploaded_file

        self.signal_wave = wave.open(self.uploaded_file, "r")

        #extract the sample rate from the file
        self.sample_rate = self.signal_wave.getframerate()

        #creat numpy array from the waveform
        self.sig = np.frombuffer(self.signal_wave.readframes(-1), dtype=np.int16)

        self.fourier = np.fft.rfft(self.sig)
        self.abs_fourier = np.abs(self.fourier)
        self.freq = np.fft.rfftfreq(self.sig.size, d=1./self.sample_rate)

        a=0
        index = -1
        for i in range(len(self.abs_fourier)):
            if self.abs_fourier[i] > a:
                a = self.abs_fourier[i]
                index = i
        self.base_freq = self.freq[index]
        self.base_freq_index = index

    def max_amp_in_range_index(self, start_freq, end_freq):
        #find the index of the starting frequency in the range
        index_start = -1
        for i in range(len(self.freq)):
            if self.freq[i] >= start_freq:
                index_start = i
                break
        #find the ending frequency index in the range
        index_end = -1
        for i in range(index_start, len(self.freq)):
            if self.freq[i] >= end_freq:
                index_end = i
                break
        #find the maximum amplitude within the frequency range (between the two indices found)
        a=0
        index = -1
        for i in range(index_start,index_end):
            if self.abs_fourier[i] > a:
                a = self.abs_fourier[i]
                index = i
        #this code is terrible, can quickly be improved by looking up bucket size and directly calculating index
        return index


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

    def plot_fourier(self, min_lim:int = 0, max_lim:int = 1000, save_plot = False):
        fig, ax = plt.subplots()
        ax.plot(self.freq,self.abs_fourier)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Absolute value of FFT")
        ax.set_yscale("log")
        ax.set_title("Fourier transform of recorded waveform")

        ax.set_xlim([min_lim,max_lim])

        cursor = Cursor(ax, color="red", linewidth=1)

        plt.show()

        if save_plot:
            plt.savefig("trial1_spectrum.png")

    def plot_base_freq_mult(self):
        fig, ax = plt.subplots()
        ax.plot(self.freq,self.abs_fourier)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Absolute value of FFT")
        ax.set_yscale("log")
        ax.set_title("Fourier transform of recorded waveform")
        #add lines
        ax.axvline(x=self.base_freq, color="red", linestyle="--", linewidth=2)
        value = 3*self.base_freq
        while value <= 1000:
            ax.axvline(x=value, color = "green", linestyle="--", linewidth=2)
            value += 2*self.base_freq

        ax.set_xlim([0,1000])

        cursor = Cursor(ax, color="red", linewidth=1)

        plt.show()
        #plt.savefig("trial1_spectrum.png")

    def plot_adjusted_base_freq(self):
        fig, ax = plt.subplots()
        ax.plot(self.freq,self.abs_fourier)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Absolute value of FFT")
        ax.set_yscale("log")
        ax.set_title("Fourier transform of recorded waveform")

        new_base_freq = self.freq[self.max_amp_in_range_index(270,380)]/3
        #add lines
        ax.axvline(x=new_base_freq, color="red", linestyle="--", linewidth=2)
        value = 3*new_base_freq
        while value <= 1000:
            ax.axvline(x=value, color = "green", linestyle="--", linewidth=2)
            value += 2*new_base_freq

        ax.set_xlim([0,1000])

        cursor = Cursor(ax, color="red", linewidth=1)

        plt.show()
        #plt.savefig("trial1_spectrum.png")

    def plot_base_freq_slider(self, slider=None):
        fig, ax = plt.subplots()
        ax.plot(self.freq,self.abs_fourier)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Absolute value of FFT")
        ax.set_yscale("log")
        ax.set_title("Fourier transform of recorded waveform")
        #add lines
        line_base = ax.axvline(x=self.base_freq, color="red", linestyle="--", linewidth=2)
        lines_multiples = [ax.axvline(self.base_freq * (2*i+1), color="green", linestyle='--') for i in range(1, 4)]
        # Slider
        if slider == None:
            axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
            slider_freq = Slider(axfreq, 'Base Frequency', 90.0, 120.0, valinit=self.base_freq)
        else:
            slider_freq = slider


        ax.set_xlim([0,1000])

        # Update function
        def update(val):
            freq = slider_freq.val
            line_base.set_xdata([freq, freq])
            for i, line in enumerate(lines_multiples):
                line.set_xdata([freq * (2*(i+1)+1), freq * (2*(i+1)+1)])
            fig.canvas.draw_idle()

        # Connect the slider and the function
        slider_freq.on_changed(update)

        cursor = Cursor(ax, color="red", linewidth=1)

        plt.show()
        #plt.savefig("trial1_spectrum.png")

    def plot_base_freq_slider_web(self,freq):
        fig, ax = plt.subplots()
        ax.plot(self.freq, self.abs_fourier)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Absolute value of FFT")
        ax.set_yscale("log")
        ax.set_title("Fourier transform of recorded waveform")
        ax.axvline(x=freq, color="red", linestyle="--", linewidth=2)
        for i in range(1, 4):
            ax.axvline(freq * (2 * i + 1), color="green", linestyle='--')
        ax.set_xlim([0, 1000])
        return fig

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
        ax.set_title("Fourier transform of recorded waveform")

        ax.set_xlim([min_lim,max_lim])

        cursor = Cursor(ax, color="red", linewidth=1)

        plt.show()
        #plt.savefig("trial1_spectrum.png")

    def get_base_amplitude(self):
        return self.base_freq_index


#trial = Sound("trimmed\guitar_tr1_trimmed_ns.wav")
# print(trial.base_freq_index)
# # trial.plot_waveform()
# trial.plot_fourier(min_lim=0,max_lim=1000)
# trial.plot_base_freq_mult()
# trial.plot_adjusted_base_freq()
#trial.plot_base_freq_slider()
#sound2 = Sound("waeyv_boy.wav")

# sound2.plot_base_freq_mult()
#trial.plot_multi_overlay(sound2)