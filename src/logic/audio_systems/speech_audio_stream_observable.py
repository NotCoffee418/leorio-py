import logic.audio_systems.audio_transformers as at
import logic.audio_systems.device_helpers as dh
import sounddevice as sd


class SpeechAudioStreamObservable:
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # singleton
        if self._is_initialized:
            return

        self._is_initialized = True
        print("boop")

        # Set hardcoded values
        self.rate = 44100
        self.channels = 2
        self.frames_per_buffer = 1024
        self.input_device_index = dh.find_seed_device_index()
        self.observers = []
        self.running = False

        self.stream = sd.InputStream(
            samplerate=self.rate,
            channels=self.channels,
            dtype='float32',
            blocksize=self.frames_per_buffer,
            device=self.input_device_index,
            callback=self._callback
        )
        self.restart()

    def _callback(self, in_data, frame_count, time_info, status):
        if not self.running:
            return

        # Seperate channels
        left, right = at.seperate_channels(in_data)

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

    def restart(self):
        try:
            self.running = True
            self.stream.start()
        except Exception as ex:
            print(f"An error occurred while starting the stream: {ex}")

    def stop(self):
        try:
            self.stream.stop()
            self.stream.close()
            self.running = False
        except Exception as ex:
            print(f"An error occurred while stopping the stream: {ex}")

    def add_observer(self, observer):
        self.observers.append(observer)
