# scripts/node/node_time.py
"""
from typing import Optional, Union

from node.node_pps_manager import get_seconds_since_midnight
from node.node_time_mode_manager import get_mode


def get_timestamp() -> Optional[Union[int, float]]:
    
    Compute and return the node’s timestamp based on PPS sync and current mode.

    Modes:
      - 'lite': integer seconds resolution
      - 'tdoa': floating-point seconds with sub-second precision

    Returns:
      int   – seconds since midnight if mode is 'lite'
      float – seconds since midnight (with fraction) if mode is 'tdoa'
      None  – if PPS sync is unavailable or mode is unrecognized
    
    mode = get_mode()
    seconds = get_seconds_since_midnight()

    # PPS not yet synced
    if seconds is None:
        return None

    if mode == "lite":
        # round to nearest second, then cast to int
        return int(round(seconds))
    elif mode == "tdoa":
        # full precision float
        return seconds
    else:
        # unrecognized mode
        return None
"""

def get_timestamp():
    return 99999.0  # Simulated timestamp for testing flow