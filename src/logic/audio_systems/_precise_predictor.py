import subprocess
from typing import List, Callable


class PrecisePredictorObservable:
    _instance = None
    _is_initialized = False
    is_paused = False
    observers: List[Callable[[str], None]] = []
    process = None

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
        self.process = None

    def pause(self):
        self.is_paused = True

    def unpause(self):
        self.is_paused = False

    def feed(self, data):
        if self.is_paused:
            return
        if self.process is not None:
            self.process.stdin.write(data)

    def subscribe(self, func: Callable[[str], None]) -> None:
        self.observers.append(func)

    def _spawn_process(self):
        self.process = subprocess.Popen(
            [self.engine_path, self.model_path, str(self.chunk_size)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def notify_all(self, data: str) -> None:
        for subscriber in self.observers:
            subscriber(data)

    def _debug_eval(self):
        self.process.stdin.close()
        stdout_data, stderr_data = self.process.communicate()
        self.notify_all(stdout_data.decode('utf-8'))
