# node_unique_id_manager.py
import time

# In-memory event cache
_event_cache = {}

# Configuration
MAX_RETRIES = 3
RETRY_TIMEOUT = 10  # seconds

def store_event(event_id, event_obj):
    _event_cache[event_id] = {
        "event_obj": event_obj,
        "timestamp": time.time(),
        "retry_count": 0,
        "acknowledged": False
    }

def acknowledge_event(event_id):
    if event_id in _event_cache:
        del _event_cache[event_id]

def get_retry_candidates():
    now = time.time()
    candidates = []
    for event_id, data in _event_cache.items():
        if not data["acknowledged"] and (now - data["timestamp"] > RETRY_TIMEOUT):
            candidates.append((event_id, data))
    return candidates

def increment_retry(event_id):
    if event_id in _event_cache:
        _event_cache[event_id]["retry_count"] += 1
        _event_cache[event_id]["timestamp"] = time.time()
        return _event_cache[event_id]["retry_count"]
    return None

def get_event(event_id):
    return _event_cache.get(event_id)

def clear_all():
    _event_cache.clear()
