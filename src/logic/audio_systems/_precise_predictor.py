import subprocess
from threading import Lock, Thread
import time
from typing import List, Callable
import logic.audio_systems.speech_audio_stream_observable as saso
import queue


class PrecisePredictorObservable:
    _instance = None
    _is_initialized = False
    is_paused = False
    observers: List[Callable[[str], None]] = []
    process: subprocess.Popen[bytes]
    ready: bool = False
    write_queue: queue.Queue[bytes] = queue.Queue()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, engine_path: str, model_path: str, chunk_size: int):
        # singleton
        if self._is_initialized:
            return

        # Init pipeline
        self.engine_path = engine_path
        self.model_path = model_path
        self.chunk_size = chunk_size

        # Precise wake word detection process
        self._spawn_process()

        # Add audio receiver function & processor
        recording_observable = saso.SpeechAudioStreamObservable()
        recording_observable.add_observer(self)

        # start threaded response precise listener
        self._feed_handler()
        self._response_handler()

    def pause(self):
        self.is_paused = True
        self.write_queue = queue.Queue()

    def unpause(self):
        self.is_paused = False

    def subscribe(self, func: Callable[[str], None]) -> None:
        self.observers.append(func)

    def _spawn_process(self):
        self.process = subprocess.Popen(
            [self.engine_path, self.model_path, str(self.chunk_size)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        self.ready = True

    def notify_all(self, data: str) -> None:
        for subscriber in self.observers:
            subscriber(data)

    # SpeechAudioStreamObservable observer callback
    def on_received(self, audio_data):
        if not self.ready or self.is_paused:
            return
        self.write_queue.put(audio_data)

    def _feed_handler(self):
        def _inner_threaded():
            while not self.ready:
                time.sleep(0.1)
            while True:
                if self.write_queue.empty():
                    time.sleep(0.1)
                    continue
                audio_data = self.write_queue.get()
                self.process.stdin.write(audio_data)
        thread = Thread(target=_inner_threaded)
        thread.start()

    # Check precise response & sends out the data to all subscribers

    def _response_handler(self):
        def _inner_threaded():
            # Wait for process to exist
            while not self.ready:
                time.sleep(0.1)

            # Run response loop
            while True:
                stdout_data, stderr_data = self.process.communicate()
                if (stderr_data):
                    raise Exception(
                        "Precise: " + stderr_data.decode("utf-8"))
                elif (stdout_data):
                    # discard responses if paused to prevent backlog
                    # send to listeners if not paused
                    if not self.is_paused:
                        self.notify_all(stdout_data.decode("utf-8"))
                time.sleep(0.1)
        thread = Thread(target=_inner_threaded)
        thread.start()
