# node_time.py
from utils.node_pps_manager import get_seconds_since_midnight
from utils.node_time_mode_manager import get_mode

def get_timestamp():
    mode = get_mode()
    seconds = get_seconds_since_midnight()
    if seconds is None:
        return None
    if mode == "lite":
        return round(seconds)  # 1-second resolution
    elif mode == "tdoa":
        return float(seconds)  # sub-second float precision
    return None