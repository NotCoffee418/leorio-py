
from precise_runner import PreciseEngine, PreciseRunner
import logic.audio_systems.processed_mic_steam as pms
import logic.audio_systems._precise_initializer as _pinit

precise_engine = None


def start_wakeword_detection(on_prediction=lambda x: None, on_activation=lambda: None):
    if not precise_engine:
        raise Exception("Precise engine not initialized")

    stream = pms.get_processed_mic_stream()
    runner = PreciseRunner(
        precise_engine,
        on_prediction=on_prediction,
        on_activation=on_activation,
        trigger_level=0,
        stream=stream)
    runner.start()


def initialize_precise():
    _pinit.ensure_install_engine()
    _pinit.ensure_install_default_model()
    global precise_engine
    precise_engine = PreciseEngine(
        _pinit.get_engine_exe_path(), _pinit.get_wakeword_model_path())
