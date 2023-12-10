from tkinter import filedialog, messagebox
import model
import view


class Controller:
    def __init__(self, root):
        self.root = root
        self.view = view.View(self)
        self.audio_instance = None

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav;*.mp3")])
        if file_path:
            try:
                self.audio_instance = model.AudioData(file_path)  # create instance of AudioData
                self.audio_instance.load_data()  # load audio data
                resonant_freq = self.audio_instance.calculate_resonant_freq() # find resonant frequency
                self.view.visualize_waveforms(resonant_freq)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the audio file: {e}")

    def calculate_rt60(self):
        if self.audio_instance:
            # pass the calculated RT60 value to the view for display or processing or sumn
            signal = self.audio_instance.audio_data
            fs = self.audio_instance.sample_rate

            # calculate RT60 for low, mid, and high frequency ranges
            low_rt60 = model.perform_frequency_range_analysis(signal, fs, (20, 500))
            mid_rt60 = model.perform_frequency_range_analysis(signal, fs, (500, 2000))
            high_rt60 = model.perform_frequency_range_analysis(signal, fs, (2000, 5000))

            # display plots of RT60 for each frequency
            self.view.display_plots(low_rt60, mid_rt60, high_rt60)

            # calculate average RT60 time
            average_rt60 = (low_rt60 + mid_rt60 + high_rt60) / 3
            # calculate the difference from 0.5 seconds
            difference = average_rt60 - 0.5

            # display the difference in the GUI
            self.view.combine_plots(difference)

    # BOY! idk
    def clean_data(self):
        if self.audio_instance:
            try:
                self.audio_instance.clean_data()
                # perform anything after cleaning data
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while cleaning the audio data: {e}")

    def perform_analysis(self):
        if self.audio_instance:
            try:
                messagebox.showinfo("Analysis",
                                    "Analysis performed successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during analysis: {e}")
