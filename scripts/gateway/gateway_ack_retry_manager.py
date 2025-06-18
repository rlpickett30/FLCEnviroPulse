# gateway_ack_retry_manager.py

import time
import threading

"""
Tracks outbound events and handles retries if ACK not received.

Every tracked event must include:
- event_id (UID)
- full_event object
- timestamp
- retry count

Built-in retry loop runs in a background thread.
"""

MAX_RETRIES = 3
RETRY_TIMEOUT = 2.5  # seconds
RETRY_LOOP_INTERVAL = 1  # seconds

_event_cache = {}
_cache_lock = threading.Lock()
_retry_thread = None
_stop_event = threading.Event()


def store_event(uid, event):
    with _cache_lock:
        _event_cache[uid] = {
            "event": event,
            "timestamp": time.time(),
            "retry_count": 0,
            "acknowledged": False
        }


def acknowledge_event(uid):
    with _cache_lock:
        if uid in _event_cache:
            del _event_cache[uid]


def get_retry_candidates():
    now = time.time()
    retry_list = []

    with _cache_lock:
        for uid, data in list(_event_cache.items()):
            if data["acknowledged"]:
                continue

            elapsed = now - data["timestamp"]
            if elapsed > RETRY_TIMEOUT:
                if data["retry_count"] < MAX_RETRIES:
                    retry_list.append(uid)
                    data["retry_count"] += 1
                    data["timestamp"] = now  #
