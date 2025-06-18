# gateway_unique_id_manager.py

import time
import threading

"""
Generates unique IDs for events that originate at the gateway or arrive without a UID.
Each UID is a monotonic counter tagged with a gateway-specific prefix if needed.
"""

_uid_lock = threading.Lock()
_uid_counter = int(time.time())  # Seed with timestamp for uniqueness across reboots


def assign_uid():
    global _uid_counter
    with _uid_lock:
        uid = _uid_counter
        _uid_counter += 1
        return uid
