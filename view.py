import tkinter as tk
from tkinter import filedialog, messagebox
import os
import librosa
import matplotlib.pyplot as plt
import numpy as np

class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Data Visualization")
        self.geometry("800x600")

        self.audio_data = None
        resonant_freq = None

        # create file_name_label widget
        self.file_name_label = tk.Label(self, text="File Name: ")
        self.file_name_label.grid(row=2, column=0, padx=10, pady=10)

        # create file_time_value label widget
        self.file_time_value_label = tk.Label(self, text="Duration: ")
        self.file_time_value_label.grid(row=3, column=0, padx=10, pady=10)

        # create widgets with functions
        load_button = tk.Button(self, text="Load Data", command=self.load_data)
        waveform_button = tk.Button(self, text="Visualize Waveforms", command=lambda: self.visualize_waveforms(resonant_freq))
        plot_button = tk.Button(self, text="Display Plots", command=self.display_plots)
        # create button for combined plot
        combine_plot_button = tk.Button(self, text="Combine Plots", command=self.combine_plots)
        visual_display_button = tk.Button(self, text="Visual Display", command=self.visual_display)
        analysis_button = tk.Button(self, text="View Analysis Results", command=self.view_analysis_results)

        # add padding
        load_button.grid(row=0, column=0, padx=10, pady=10)
        waveform_button.grid(row=0, column=1, padx=10, pady=10)
        plot_button.grid(row=1, column=0, padx=10, pady=10)
        combine_plot_button.grid(row=1, column=1, padx=10, pady=10)
        visual_display_button.grid(row=1, column=2, padx=10, pady=10)
        analysis_button.grid(row=0, column=2, padx=10, pady=10)

        # start main loop
        self.mainloop()

    def load_data(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav;*.mp3")])
            if file_path:  # check if a file is selected
                self.audio_data, sample_rate = librosa.load(file_path)
                file_name = os.path.basename(file_path)
                self.file_name_label.config(text=f"File Name: {file_name}")
                file_time_value = librosa.get_duration(y=self.audio_data, sr=sample_rate)
                self.file_time_value_label.config(text=f"Duration: {file_time_value:.2f} seconds")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the audio file: {e}")

    def visualize_waveforms(self, resonant_freq):
        try:
            if self.audio_data is not None:
                self.controller.visualize_waveforms(resonant_freq)
                # Plot the waveform
                plt.figure(figsize=(10, 4))
                plt.plot(self.audio_data)
                plt.title('Waveform')
                plt.xlabel('Time')
                plt.ylabel('Amplitude')
                plt.text(0.5, 0.9, f'Resonance: {resonant_freq:.2f} Hz', transform=plt.gca().transAxes,
                         color='red')
                plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while visualizing waveforms: {e}")

    def display_plots(self, low_rt60, mid_rt60, high_rt60):
        try:
            if self.audio_data is not None:
                self.controller.display_plots(low_rt60, mid_rt60, high_rt60)
                time_values = np.linspace(0, len(self.audio_data) / librosa.get_samplerate(self.audio_data),
                                          len(self.audio_data))

                plt.figure(figsize=(12, 6))

                plt.subplot(3, 1, 1)
                plt.plot(time_values, low_rt60)
                plt.title('Low Frequency RT60')
                plt.xlabel('Time (s)')
                plt.ylabel('Power (dB)')
                plt.legend()

                plt.subplot(3, 1, 2)
                plt.plot(time_values, mid_rt60)
                plt.title('Mid Frequency RT60')
                plt.xlabel('Time (s)')
                plt.ylabel('Power (dB)')
                plt.legend()

                plt.subplot(3, 1, 3)
                plt.plot(time_values, high_rt60)
                plt.title('High Frequency RT60')
                plt.xlabel('Time (s)')
                plt.ylabel('Power (dB)')
                plt.legend()

                plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while displaying plots: {e}")

    def combine_plots(self, difference):
        try:
            if self.audio_data is not None:
                time_values = np.linspace(0, len(self.audio_data) / librosa.get_samplerate(self.audio_data),
                                          len(self.audio_data))

                plt.figure(figsize=(10, 4))

                # Plot combined RT60 values with different colors
                plt.plot(time_values, self.controller.low_rt60, label='Low Frequency RT60', color='red')
                plt.plot(time_values, self.controller.mid_rt60, label='Mid Frequency RT60', color='blue')
                plt.plot(time_values, self.controller.high_rt60, label='High Frequency RT60', color='green')

                plt.title('Combined RT60')
                plt.xlabel('Time (s)')
                plt.ylabel('Power (dB)')
                plt.legend()

                # show difference in RT60 value to reduce to 0.5 seconds
                plt.text(0.5, 0.9, f'Difference: {self.controller.combine_plots(difference):.2f} seconds',
                         transform=plt.gca().transAxes,
                         color='red')

                plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while combining plots: {e}")

    def visual_display(self):
        try:
            if self.audio_data is not None:
                # create a spectrogram
                plt.figure(figsize=(10, 4))
                librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(self.audio_data)), ref=np.max),
                                         y_axis='log', x_axis='time')
                plt.title('Spectrogram')
                plt.colorbar(format='%+2.0f dB')
                plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while displaying visual display: {e}")

    # shiiiii
    def view_analysis_results(self):
        try:
            analysis_results = "Sample analysis results:\nMean: 5.6\nStandard Deviation: 2.3\nMax Value: 10.1"  # placeholder results
            messagebox.showinfo("Analysis Results", analysis_results)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while viewing analysis results: {e}")