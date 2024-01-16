import tkinter as tk
import pyaudio
import wave
import threading

class AudioCaptureApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Capture App")

        self.record_button = tk.Button(self.master, text="Record", command=self.start_recording)
        self.record_button.pack(pady=10)

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(self.master, text="Status: Ready")
        self.status_label.pack(pady=10)

    def start_recording(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                 channels=1,
                                 rate=44100,
                                 input=True,
                                 frames_per_buffer=1024)

        self.frames = []
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Recording")

        # Start a new thread for recording
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

    def record_audio(self):
        while True:
            try:
                data = self.stream.read(1024)
                self.frames.append(data)
            except Exception as e:
                break

#     self.stream.stop_stream()
    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        # Save the recorded audio to a WAV file
        wf = wave.open("output.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b"".join(self.frames))
        wf.close()

        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Ready")

def main():
    root = tk.Tk()
    app = AudioCaptureApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
