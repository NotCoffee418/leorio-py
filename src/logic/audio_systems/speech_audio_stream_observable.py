import pyaudio
import numpy as np

class SpeechAudioStreamObservable:
    def __init__(self):
        # Set hardcoded values
        self.rate = 16000
        self.channels = 1
        self.format = pyaudio.paInt16
        self.frames_per_buffer = 1024
        self.observers = []

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.frames_per_buffer,
            stream_callback=self._callback
        )

    def _callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)

        # Amplify volume (Be cautious of clipping)
        audio_data = np.clip(audio_data * 2, -32768, 32767)

        # Notify observers
        for observer in self.observers:
            observer.on_received(audio_data.tobytes())

        return (audio_data.tobytes(), pyaudio.paContinue)

    def start(self):
        try:
            self.stream.start_stream()
        except Exception as ex:
            print(f"An error occurred while starting the stream: {ex}")

    def stop(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
        except Exception as ex:
            print(f"An error occurred while stopping the stream: {ex}")

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

# Example observer class for PreciseRunner
class ExamplePreciseObserver:
    def __init__(self, runner):
        self.runner = runner

    def update(self, audio_data):
        self.runner.update(audio_data)
        print(f"Sent {len(audio_data)} bytes of audio data to PreciseRunner.")

# # Usage (assuming 'runner' is an instance of PreciseRunner)
# if __name__ == "__main__":
#     from your_precise_runner_library import PreciseRunner  # Replace this with actual import

#     runner = PreciseRunner(...)  # Initialize your PreciseRunner instance here

#     audio_stream_observable = SpeechAudioStreamObservable()
#     precise_observer = ExamplePreciseObserver(runner)

#     audio_stream_observable.add_observer(precise_observer)
#     audio_stream_observable.start()

#     try:
#         while True:
#             pass
#     except KeyboardInterrupt:
#         audio_stream_observable.stop()
