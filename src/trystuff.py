import logic.audio_systems.precise_access as precise
import logic.audio_systems.audio_experiments as rectest
# precise.initialize_precise()
# precise.start_wakeword_detection(lambda x: print(x), lambda: print("active"))

rectest.list_audio_devices_and_rates()


rectest.record_wav_test()
