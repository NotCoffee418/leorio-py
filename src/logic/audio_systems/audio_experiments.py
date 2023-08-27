import wave
import time
from logic.audio_systems.speech_audio_stream_observable import SpeechAudioStreamObservable
import logic.utils.io_access as io
import pyaudio
import sys, os

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


def record_wav_test():
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


def list_audio_devices_and_rates():
    p = pyaudio.PyAudio()
    
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    
    for i in range(0, num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        
        if "seeed-2mic-voicecard" in device_info.get('name'):
            print(f"Input Device ID {i} - {device_info.get('name')}")
            print("  Supported Sample Rates:")
            
            for rate in [8000, 11025, 16000, 22050, 44100, 48000, 88200, 96000, 192000]:
                try:
                    if p.is_format_supported(input_format=pyaudio.paInt16,
                                             input_channels=device_info['maxInputChannels'],
                                             rate=rate,
                                             input_device=device_info['index']):
                        print(f"    {rate} Hz")
                except ValueError as e:
                    print(f"    Not supported: {rate} Hz")