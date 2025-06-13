# node/node_unique_id_manager.py

import threading
import time
from pathlib import Path

# === Unique ID Generator ===
class UniqueIdManager:
    _lock = threading.Lock()

    def __init__(self, persistence_file: str = None):
        self._counter = 0
        self._start_time = int(time.time()) & 0xFFFF_FFFF
        self._persistence_file = persistence_file
        if persistence_file:
            self._load_counter()

    def _load_counter(self):
        path = Path(self._persistence_file)
        if path.exists():
            try:
                self._counter = int(path.read_text().strip())
            except Exception:
                self._counter = 0

    def _save_counter(self):
        if self._persistence_file:
            path = Path(self._persistence_file)
            path.parent.mkdir(parents=True, exist_ok=True)  # <--- ensure folder exists
            path.write_text(str(self._counter))
        
    def next_id(self) -> int:
        with UniqueIdManager._lock:
            uid = ((self._start_time << 16) & 0xFFFF_0000) | (self._counter & 0xFFFF)
            self._counter = (self._counter + 1) & 0xFFFF
            self._save_counter()
            return uid

# === In-Memory Event Cache for ACK/Retry ===
# Configuration
MAX_RETRIES = 3
RETRY_TIMEOUT = 10  # seconds

_event_cache = {}

def store_event(event_id, event_obj):
    _event_cache[event_id] = {
        "event_obj": event_obj,
        "timestamp": time.time(),
        "retry_count": 0,
        "acknowledged": False
    }

def acknowledge_event(event_id):
    _event_cache.pop(event_id, None)

def get_retry_candidates():
    now = time.time()
    return [
        (eid, data)
        for eid, data in _event_cache.items()
        if not data["acknowledged"] and (now - data["timestamp"] > RETRY_TIMEOUT)
    ]

def increment_retry(event_id):
    if event_id in _event_cache:
        entry = _event_cache[event_id]
        entry["retry_count"] += 1
        entry["timestamp"] = time.time()
        return entry["retry_count"]
    return None

def get_event(event_id):
    return _event_cache.get(event_id)

def clear_all():
    _event_cache.clear()

