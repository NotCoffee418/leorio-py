import pyaudio


def find_seed_device_index():
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()
    target_description = "seeed-2mic-voicecard"

    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        if device_info.get('maxInputChannels') > 0:
            device_name = device_info.get('name')
            if target_description in device_name:
                p.terminate()
                return i

    p.terminate()
    raise Exception(
        f"Device with description containing '{target_description}' not found")
