import pyaudio
import logic.audio_systems.speech_audio_stream_observable as saso


def get_processed_mic_stream():
    class StreamMicProcessedObserver:
        def __init__(self, output_stream):
            self.listening = True
            self.output_stream = output_stream

        def on_received(self, audio_data):
            if self.listening:
                self.output_stream.write(audio_data)

    # Set up the pyaudio result stream
    p = pyaudio.PyAudio()
    output_stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
        input_device_index=None)

    # Initialize the observer and add to the audio stream
    input_observer = StreamMicProcessedObserver(output_stream)
    inptut_observable = saso.SpeechAudioStreamObservable()
    inptut_observable.add_observer(input_observer)
    return output_stream
