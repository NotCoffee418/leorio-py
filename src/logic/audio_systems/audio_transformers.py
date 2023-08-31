from scipy.signal import butter, filtfilt
import numpy as np


def bytes_to_np(bytes_data):
    return np.frombuffer(bytes_data, dtype=np.float32)


def np_to_bytes(np_data):
    return np_data.tobytes()


def filter_human_speech_only(np_channel, sample_rate):
    # Normalize the audio data
    np_channel_normalized = np_channel / 32768.0

    # Filter design parameters
    order = 5
    nyquist = 0.5 * sample_rate
    low = 300.0 / nyquist
    high = 3400.0 / nyquist

    # Design and apply the filter
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, np_channel_normalized)

    # Scale back and clip the values to int16 range
    y = np.clip(y * 32768.0, -32768, 32767)

    # Convert the datatype to int16
    y = y.astype(np.int16)
    return y


def volume_boost(np_channel, volume_ratio):
    # Volume boost & prevent clipping
    return np.clip(np_channel * volume_ratio, -32768, 32767)


def seperate_channels(np_data):
    left_channel = np_data[::2]
    right_channel = np_data[1::2]
    return left_channel, right_channel


def merge_two_channels(np_left_channel, np_right_channel):
    return (np_left_channel + np_right_channel) // 2
