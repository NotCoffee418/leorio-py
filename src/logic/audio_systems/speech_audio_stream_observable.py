import pyaudio
import logic.audio_systems.audio_transformers as at

# Records and transforms audio to single channel, 16-bit PCM, 16kHz sample rate


class SpeechAudioStreamObservable:
    def __init__(self):
        # Set hardcoded values
        self.rate = 16000
        self.channels = 2
        self.format = pyaudio.paInt16
        self.frames_per_buffer = 1024
        self.input_device_index = find_seed_device_index()
        self.observers = []

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input_device_index=self.input_device_index,
            input=True,
            frames_per_buffer=self.frames_per_buffer,
            stream_callback=self._callback
        )

    def _callback(self, in_data, frame_count, time_info, status):
        # Convert to np & seperate stereo channels
        np_input = at.bytes_to_np(in_data)
        np_left, np_right = at.seperate_channels(np_input)

        # Filter to human speech frequencies
        # WIP: We need fix whitenoise first, then test again
        # np_left = at.filter_human_speech_only(np_left, self.rate)
        # np_right = at.filter_human_speech_only(np_right, self.rate)

        # Volume boost
        np_left = at.volume_boost(np_left, 3)
        np_right = at.volume_boost(np_right, 3)

        # Merge channels to single mono channel & back to binary
        np_input = at.merge_two_channels(np_left, np_right)
        out_data = at.np_to_bytes(np_input)

        # Notify observers
        for observer in self.observers:
            observer.on_received(out_data)
        return (out_data, pyaudio.paContinue)

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


def find_seed_device_index():
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()
    target_description = "seeed-2mic-voicecard"

    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        if device_info.get('maxInputChannels') > 0:
            device_name = device_info.get('name')
            if target_description in device_name:
                p.terminate()
                return i

    p.terminate()
    raise Exception(
        f"Device with description containing '{target_description}' not found")


# Example observer class for PreciseRunner
# class ExamplePreciseObserver:
#     def __init__(self, runner):
#         self.runner = runner

#     def update(self, audio_data):
#         self.runner.update(audio_data)
#         print(f"Sent {len(audio_data)} bytes of audio data to PreciseRunner.")

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
