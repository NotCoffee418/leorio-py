import pyaudio
import logic.audio_systems.audio_transformers as at
import logic.audio_systems.device_helpers as dh


class SpeechAudioStreamObservable:
    def __init__(self):
        # Set hardcoded values
        self.rate = 44100
        self.channels = 2
        self.format = pyaudio.paFloat32
        self.frames_per_buffer = 1024
        self.input_device_index = dh.find_seed_device_index()
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
        np_f32 = at.bytes_to_float32(in_data)
        left, right = at.seperate_channels(np_f32)

        # Filter to human speech frequencies
        # WIP: We need fix whitenoise first, then test again
        # left = filter_human_speech_only(left, self.rate)
        # right = filter_human_speech_only(right, self.rate)

        # Volume boost
        # left = volume_boost(left, volume_rate)
        # right = volume_boost(right, volume_rate)

        # Merge channels to single mono channel
        np_f32 = at.merge_two_channels(left, right)

        # Clip to prevent overload
        np_f32 = at.clip_float32(np_f32)

        # Convert to int16 binary for output
        np_i16 = at.float32_to_int16(np_f32)
        out_binary_i16 = at.int16_to_bytes(np_i16)

        # Report data to observer
        for observer in self.observers:
            observer.on_received(out_binary_i16)
        return (np_f32, pyaudio.paContinue)

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
