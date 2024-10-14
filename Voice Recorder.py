import tkinter as tk
import sounddevice as sd
import wavio as wv
import threading

# Initialize tkinter window
root = tk.Tk()
root.title("Voice Recorder")
root.geometry("400x200")

# Global variables for recording
fs = 44100  # Sample rate
duration = 10  # Default recording duration in seconds
is_recording = False


# Function to start recording
def start_recording():
    global is_recording
    is_recording = True
    record_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    def record_audio():
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait for the recording to finish
        wv.write("output.wav", recording, fs, sampwidth=2)  # Save the recording

    # Use a thread to not block the GUI
    threading.Thread(target=record_audio).start()


# Function to stop recording
def stop_recording():
    global is_recording
    is_recording = False
    sd.stop()  # Stop recording if it's running
    record_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)


# Function to set recording duration
def set_duration(value):
    global duration
    duration = int(value)


# GUI layout
label = tk.Label(root, text="Voice Recorder", font=("Arial", 16))
label.pack(pady=10)

duration_label = tk.Label(root, text="Set Duration (Seconds):", font=("Arial", 12))
duration_label.pack(pady=5)

duration_slider = tk.Scale(root, from_=1, to=60, orient=tk.HORIZONTAL, command=set_duration)
duration_slider.set(duration)
duration_slider.pack(pady=5)

record_button = tk.Button(root, text="Start Recording", font=("Arial", 12), command=start_recording)
record_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Recording", font=("Arial", 12), state=tk.DISABLED, command=stop_recording)
stop_button.pack(pady=5)

# Start the GUI loop
root.mainloop()
