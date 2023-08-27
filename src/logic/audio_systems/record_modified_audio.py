import wave
import time
from logic.audio_systems.speech_audio_stream_observable import SpeechAudioStreamObservable
import logic.utils.io_access as io

def record_wav_test():
    class WavFileObserver:
        def __init__(self, filename, rate, channels, duration):
            self.filename = filename
            self.rate = rate
            self.channels = channels
            self.duration = duration
            self.audio_data = bytearray()
            self.frames = int(rate * duration)
            self.frame_count = 0

        def on_received(self, audio_data):
            self.audio_data.extend(audio_data)
            self.frame_count += len(audio_data) // (self.channels * 2)  # 2 bytes per sample
            if self.frame_count >= self.frames:
                with wave.open(self.filename, 'wb') as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(2)  # 2 bytes
                    wf.setframerate(self.rate)
                    wf.writeframes(self.audio_data)




    audio_stream_observable = SpeechAudioStreamObservable()
    
    # Initialize the observer and add to the audio stream
    wav_observer = WavFileObserver(io.get_path('data', 'test.wav'), 16000, 1, 3)
    audio_stream_observable.add_observer(wav_observer)
    
    # Start the audio stream
    audio_stream_observable.start()

    try:
        print("Recording audio for 3 seconds...")
        # Recording will be for 3 seconds
        time.sleep(3)
    finally:
        print("Done recording.")
        audio_stream_observable.stop()
