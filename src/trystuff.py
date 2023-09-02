import logic.audio_systems.wakeword_access as precise
import logic.audio_systems.audio_experiments as rectest

# -- Wake word
precise.initialize_precise()
precise.start_wakeword_detection(lambda x: print(x), lambda: print("active"))

# -- Record Sound
#rectest.list_audio_devices_and_rates()
#rectest.record_wav_test()
