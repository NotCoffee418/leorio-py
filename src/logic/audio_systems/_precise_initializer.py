import os
import urllib.request
import tarfile
import logic.utils.io_access as io


def get_engine_exe_path():
    return io.get_path('data', 'precise-engine', 'precise-engine')


def get_wakeword_model_path(override_model_filename=None):
    model_filename = override_model_filename or os.getenv(
        'WAKEWORD_MODEL_FILENAME')
    if model_filename is None:
        raise Exception(
            "WAKEWORD_MODEL_FILENAME not set and no model filename provided")
    return io.get_path('data', 'precise-models', model_filename)


def ensure_install_engine(crash=False):
    exe_path = get_engine_exe_path()

    # Already exists, go home
    if os.path.exists(exe_path):
        return
    elif crash:
        raise Exception("Precise Engine not found and failed to install")

    # Install it
    print("Installing precise-engine...")
    url = "https://github.com/MycroftAI/precise-data/raw/dist/armv7l/precise-engine.tar.gz"
    download_path = io.get_path("data", "precise-engine.tar.gz")
    extract_path = io.get_path("data")

    urllib.request.urlretrieve(url, download_path)
    with tarfile.open(download_path, "r:gz") as tar:
        tar.extractall(path=extract_path)

    # Clean up: remove the downloaded tar.gz file
    os.remove(download_path)
    print("Precise Engine installed")
    ensure_install_engine(crash=True)


def ensure_install_default_model(crash=False):
    model_path = get_wakeword_model_path('hey-mycroft-en.pb')  # default model

    # Already exists, go home
    if os.path.exists(model_path):
        return
    elif crash:
        raise Exception(
            "Precise default model not found and failed to install")

    # Install it
    print("Installing precise-engine...")
    url = "https://github.com/MycroftAI/precise-data/raw/models/hey-mycroft.tar.gz"
    download_path = io.get_path("data", "default-wakeword.tar.gz")
    extract_path = io.get_path("data", "precise-models")

    urllib.request.urlretrieve(url, download_path)
    with tarfile.open(download_path, "r:gz") as tar:
        tar.extractall(path=extract_path)

    # Clean up: remove the downloaded tar.gz file
    os.remove(download_path)
    print("Precise Engine installed")
    ensure_install_engine(crash=True)
