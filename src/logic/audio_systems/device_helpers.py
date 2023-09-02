import sounddevice as sd


def find_seed_device_index():
    devices = sd.query_devices()
    target_description = "seeed-2mic-voicecard"

    for i, device in enumerate(devices):
        if device['name'].startswith(target_description):
            return i

    raise Exception(
        f"Device with description containing '{target_description}' not found")
