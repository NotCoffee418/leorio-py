import threading
import subprocess
import logic.audio_systems._precise_predictor as pp
import logic.audio_systems.wakeword_access as precise
import logic.audio_systems.audio_experiments as rectest
import logic.utils.io_access as io
import time
# -- Wake word
# precise.initialize_precise()
# precise.start_wakeword_detection(lambda x: print(x), lambda: print("active"))

# -- Record Sound
# rectest.list_audio_devices_and_rates()
# rectest.record_wav_test()

engine_path: str = io.get_path('data', 'precise-engine', 'precise-engine')
model_path: str = io.get_path('data', 'precise-models', 'hey-mycroft.pb')
chunk_size: int = 2048
# precise_observer = pp.PrecisePredictorObservable(engine, model, chunk_size)
# precise_observer.subscribe(lambda x: print(x))
# print("go")
# # time.sleep(5)

# print("stop")
# # precise_observer.test_close()
# input("lock")

process = subprocess.Popen(
    [engine_path, model_path, str(chunk_size)],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)

lock = threading.Lock()
def threaded_hell():
    time.sleep(20)
    while True:
        with lock:
            r = process.stdin.write(bytes([0] * chunk_size))
            print(r)
        time.sleep(2)


threading.Thread(target=threaded_hell).start()


while True:
    with lock:
        stdout_data, stderr_data = process.poll()
        print(stdout_data)
        print(stderr_data)
    time.sleep(1)
