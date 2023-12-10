# Audio Analysis Project

This project is about analyzing audio files using Python. It provides an interface that works with audio data, analyzes and visualizes the results.

## Purpose

The goal of this project is to offer a user-friendly way to explore audio files, extract useful information, and visualize it. It's designed to handle tasks like loading different audio formats, cleaning data, and conducting basic analyses.

## Contents

### model.py

Contains the `AudioData` class, which handles the core functionalities:

- Loading audio data from files (supports .wav and .mp3 formats).
- Cleaning the data for consistency and ease of analysis.

### view.py

Implements the GUI for interacting with audio files:

- Provides buttons for loading audio, visualizing waveforms, displaying plots, and viewing analysis results.

### controller.py

Acts as the median between the data and the interface:

- Implements actions like loading, cleaning, analyzing, and displaying results.
- Connects the backend data operations with the frontend user interface.

### project_test.py

Contains the main script to run the application

## Usage

### Installation

Install required libraries by running: 

```bash
pip install -r requirements.txt
```

### Running the Application

In your terminal, execute:

```bash
python project_test.py
