import numpy as np
from scipy.signal import butter, filtfilt


def bytes_to_float32(bytes_data):
    return np.frombuffer(bytes_data, dtype=np.float32)


def bytes_to_int16(bytes_data):
    return np.frombuffer(bytes_data, dtype=np.int16)


def float32_to_bytes(np_data):
    return np_data.astype(np.float32).tobytes()


def int16_to_bytes(np_data):
    return np_data.astype(np.int16).tobytes()


def float32_to_int16(float32_array):
    # Clip, prevent overload
    float32_array = np.clip(float32_array, -1.0, 1.0)

    # Scale it to int16 values
    float32_array = np.round(float32_array * 32767)

    # Cast and return it
    return float32_array.astype(np.int16)


def filter_human_speech_only(np_channel, sample_rate):
    # Ensure the data type
    np_channel = np_channel.astype(np.float32)

    # Normalize the audio data if it is not already between -1 and 1
    if np.max(np.abs(np_channel)) > 1:
        np_channel = np_channel / np.max(np.abs(np_channel))

    # Filter design parameters
    order = 5  # <-- You might want to adjust this
    nyquist = 0.5 * sample_rate
    low = 300.0 / nyquist
    high = 3400.0 / nyquist

    # Design and apply the filter
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, np_channel)

    # Make sure the output is in float32 format
    y = y.astype(np.float32)

    return y


def volume_boost(np_channel, volume_ratio):
    # Volume boost & prevent clipping
    return np.clip(np_channel * volume_ratio, -1, 1)


def seperate_channels(np_data):
    left_channel = np_data[::2]
    right_channel = np_data[1::2]
    return left_channel, right_channel


def merge_two_channels(np_left_channel, np_right_channel):
    return (np_left_channel / 2) + (np_right_channel / 2)


def clip_float32(np_data):
    return np.clip(np_data, -1, 1)
