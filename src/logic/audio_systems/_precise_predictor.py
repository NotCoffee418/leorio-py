import subprocess

class PrecisePredictorObservable:
    _instance = None
    _is_initialized = False
    is_paused = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, engine_path, model_path):
        # singleton
        if self._is_initialized:
            return

        # Init pipeline
        io.get
        process = subprocess.Popen(['grep', 'hello'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def pause(self):
        self.is_paused = True

    def unpause(self):
        self.is_paused = False
