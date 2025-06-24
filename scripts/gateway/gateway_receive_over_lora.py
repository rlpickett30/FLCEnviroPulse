# gateway_receive_over_lora.py

import os
import sys
import time
import threading


# Set up project root for relative imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Core system import
from gateway.gateway_lora_packet_source import receive_packet as receive_lora_packet



def listen_for_lora_packets():
    print("[LORA LISTENER] Started.")
    while True:
        print("[LOOP] About to call receive_packet()")
        packet = receive_lora_packet()

        if packet is None:
            time.sleep(0.1)
            continue

        print(f"[LOOP] Raw packet received: {packet.hex()}")

if __name__ == "__main__":
    threading.Thread(target=listen_for_lora_packets, daemon=True).start()
    while True:
        time.sleep(1)
