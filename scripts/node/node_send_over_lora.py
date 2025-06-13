# node_send_over_lora.py

import sys
from node.node_unique_id_manager import UniqueIdManager
from node.node_unique_id_manager import store_event

uid_gen = UniqueIdManager(persistence_file="config/uid_counter.txt")

try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    serial = None
    SERIAL_AVAILABLE = False

class LoRaSender:
    # … your existing __init__ …

    def send(self, event_obj):
        # 1. generate unique ID
        uid = uid_gen.next_id()

        # 2. build your binary with that uid
        packet = protocol.encode_event_with_uid(event_obj, uid)

        # 3. cache for potential retries
        store_event(uid, event_obj)

        # 4. actually send/simulate
        if self.ser:
            self.ser.write(packet + b'\n')
        else:
            print(f"[LoRaSender] (simulated) payload → {packet!r}")