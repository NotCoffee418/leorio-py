import pyaudio
import logic.audio_systems.speech_audio_stream_observable as saso
import queue


def get_processed_mic_stream():
    class StreamMicProcessedObserver:
        def __init__(self, output_stream):
            self.listening = True
            self.output_stream = output_stream

        def on_received(self, audio_data):
            if self.listening:
                self.output_stream.write(audio_data)

    # Set up the pyaudio result stream
    # p = pyaudio.PyAudio()
    # output_stream = p.open(
    #     format=pyaudio.paInt16,
    #     channels=1,
    #     rate=48000,
    #     input=True,
    #     output=True,
    #     frames_per_buffer=1024)
    output_stream = FakePyAudioStream()

    # Initialize the observer and add to the audio stream
    input_observer = StreamMicProcessedObserver(output_stream)
    inptut_observable = saso.SpeechAudioStreamObservable()
    inptut_observable.add_observer(input_observer)
    return output_stream


class FakePyAudioStream:
    def __init__(self):
        self.buffer = queue.Queue()

    def read(self, num_frames, exception_on_overflow=False):
        data = bytearray()
        # Make sure to read exactly 'num_frames' frames
        for _ in range(num_frames):
            if self.buffer.empty():
                if (exception_on_overflow):
                    raise IOError("Buffer is empty")
                data.append(0)
            else:
                data.append(self.buffer.get())

        return bytes(data)

    def write(self, audio_data):
        for b in audio_data:
            self.buffer.put(b)
