import librosa
import librosa.display
import numpy as np
from scipy import stats
from scipy.fft import fft, fftfreq
from scipy.io.wavfile import write
from scipy.signal import welch
import os

class AudioData:
   def __init__(self, file_path):
       self.file_path = file_path
       self.audio_data = None
       self.sample_rate = None
       self.duration = None

   def load_data(self):
       self.audio_data, self.sample_rate = librosa.load(self.file_path, sr=None)
       self.duration = librosa.get_duration(y=self.audio_data, sr=self.sample_rate)

   def clean_data(self):
       self.audio_data, _ = librosa.load(self.file_path, sr=None,
                                         mono=True)  # removes meta data & handles multi-channel - hannah

   def format_data(self):  # Checks for wav and mp3, if not, convert to wav - hannah
       if not self.file_path.lower().endswith(('.wav', '.mp3')):
           wav_file_path = os.path.splitext(self.file_path)[0] + '.wav'
           write(wav_file_path, self.sample_rate, (self.audio_data * 32767).astype(np.int16))
           self.audio_data, _ = librosa.load(wav_file_path, sr=None, mono=True)
           self.file_path = wav_file_path

   def calculate_resonant_freq(self):
       frequencies, power = welch(self.audio_data, fs=self.sample_rate)
       resonant_freq = frequencies[np.argmax(power)]
       return resonant_freq

   def calculate_rt60(self):
       signal = self.audio_data
       fs = self.sample_rate

       # calculate RT60 for low, mid, and high frequency ranges
       low_rt60 = perform_frequency_range_analysis(signal, fs, (20, 500))
       mid_rt60 = perform_frequency_range_analysis(signal, fs, (500, 2000))
       high_rt60 = perform_frequency_range_analysis(signal, fs, (2000, 5000))

       # calculate average RT60 time
       average_rt60 = (low_rt60 + mid_rt60 + high_rt60) / 3

       # calculate the difference from 0.5 seconds
       difference = average_rt60 - 0.5

       return low_rt60, mid_rt60, high_rt60, difference


file_path_global = "/Users/hanna/PycharmProjects/pythonProject/projectFiles/PolyHallClap_10mM.wav"


audio_instance = AudioData(file_path_global)


audio_instance.load_data()




def calculate_summary_statistics(data):
   mean = np.mean(data)
   median = np.median(data)
   mode = stats.mode(data)
   std_dev = np.std(data)
   variance = np.var(data)
   return mean, median, mode, std_dev, variance




def perform_frequency_range_analysis(signal, fs, frequency_range):
   # perform FFT on the signal
   n = len(signal)
   freqs = fftfreq(n, 1 / fs)
   fft_vals = fft(signal)


   # define frequency range indices
   min_freq, max_freq = frequency_range
   freq_range_indices = np.where((freqs >= min_freq) & (freqs <= max_freq))[0]


   # extract FFT values within the specified frequency range
   freq_range_fft = fft_vals[freq_range_indices]


   return freq_range_fft, freqs[freq_range_indices]
