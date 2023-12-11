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
               self.audio_instance = model.AudioData(file_path)
               self.audio_instance.load_data()
               self.view.display_file_name(self.audio_instance.file_path)
               self.view.display_file_duration(self.audio_instance.file_path)

               resonant_freq = self.audio_instance.calculate_resonant_freq
               self.view.visualize_waveforms(resonant_freq)

               # display plots of RT60 for each frequency
               low_rt60, mid_rt60, high_rt60, difference = self.audio_instance.calculate_rt60()
               self.view.display_plots(low_rt60, mid_rt60, high_rt60)

               self.view.combine_plots(difference)

           except Exception as e:
               messagebox.showerror("Error", f"An error occurred while loading the audio file: {e}")

   def clean_data(self):
       if self.audio_instance:
           try:
               self.audio_instance.clean_data()

           except Exception as e:
               messagebox.showerror("Error", f"An error occurred while cleaning the audio data: {e}")


   def perform_analysis(self):
       if self.audio_instance:
           try:
               messagebox.showinfo("Analysis",
                                   "Analysis performed successfully.")

           except Exception as e:
               messagebox.showerror("Error", f"An error occurred during analysis: {e}")
