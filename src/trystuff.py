import logic.audio_systems._precise_predictor as pp
import logic.audio_systems.wakeword_access as precise
import logic.audio_systems.audio_experiments as rectest
import logic.utils.io_access as io

# -- Wake word
# precise.initialize_precise()
# precise.start_wakeword_detection(lambda x: print(x), lambda: print("active"))

# -- Record Sound
# rectest.list_audio_devices_and_rates()
# rectest.record_wav_test()


precise_observer = pp.PrecisePredictorObservable(
    io.get_path('data', 'precise-engine', 'precise-engine'),
    io.get_path('data', 'precise-models', 'hey-mycroft-en.pb'),
    2048
)
precise_observer.subscribe(lambda x: print(x))
