# gateway_node_simulator.py
import json
import os
import time

from utils.protocol import Protocol
from gateway.gateway_lora_inbound_object_builder import decode_wrapped_packet
from gateway.gateway_dispatcher import dispatch_event
from gateway.gateway_sanity_check import sanity_check
from gateway.gateway_object_constructor import construct_gateway_event


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NODE_REGISTRY_PATH = os.path.join(SCRIPT_DIR, "..", "config", "registers", "node_registry.json")

def load_node_registry():
    with open(NODE_REGISTRY_PATH, "r") as f:
        return json.load(f)
"""

Simulates raw inbound LoRa events from node to gateway:
- Decodes binary payload
- Runs sanity check
- Constructs full node event
- Routes to dispatcher
- Displays registry before/after
"""

protocol = Protocol("config/maps")

def split_hex_chunks(hex_str, field_lengths):
    chunks = []
    i = 0
    for byte_len in field_lengths:
        chunks.append(hex_str[i:i + (byte_len * 2)])
        i += (byte_len * 2)
    return chunks

def show_registry_state(tag=""):
    print(f"\n[{tag} REGISTRY STATE]")
    print(json.dumps(load_node_registry(), indent=2))

def simulate_inbound_event(raw_bytes, label, field_lengths):
    print(f"\n[SIM] Simulating: {label}")
    print("[RAW]:", raw_bytes.hex())
    chunks = split_hex_chunks(raw_bytes.hex(), field_lengths)
    print("[DELIM]:", " | ".join(chunks))

    show_registry_state("BEFORE")

    wrapped_packet = {
        "gateway_header": {
            "gateway_id": "SIM_GATEWAY",
            "gateway_time": int(time.time())
        },
        "raw_payload": raw_bytes
    }

    event = decode_wrapped_packet(wrapped_packet)
    
    if not event or event.get("event_type") == "error":
        print("[ERROR] Decoding failed.")
        return

    dispatch_event(event)

    if not event or event.get("event_type") == "error":
        print("[ERROR] Decoding failed.")
        return

    dispatcher = dispatch_event()
    dispatcher.route_event(event)

    show_registry_state("AFTER")


def run_node_simulator():
    while True:
        print("\n[NODE SIM MENU]")
        print("1. Avis Lite Detection")
        print("2. Avis TDOA Detection")
        print("3. Telemetry Packet")
        print("4. Weather Packet")
        print("5. Start Project Ack")
        print("6. Ack/Retry Response")
        print("7. Quit")

        choice = input("Choose simulation: ").strip()

        if choice == "1":
            simulate_inbound_event(
                bytes.fromhex("01000000010015040100000001"),
                    "Avis Lite Detection", [1, 4, 2, 1, 1, 4]
            )

        elif choice == "2":
            simulate_inbound_event(
                bytes.fromhex("0100000002010401"),
                "Avis TDOA Detection", [1, 4, 1, 1, 2]
            )
        elif choice == "3":
            simulate_inbound_event(
                bytes.fromhex("0200000003040102"),
                "Telemetry Packet", [1, 4, 1, 1, 2]
            )
        elif choice == "4":
            simulate_inbound_event(
                bytes.fromhex("0300000004040103"),
                "Weather Packet", [1, 4, 1, 1, 2]
            )
        elif choice == "5":
            simulate_inbound_event(
                bytes.fromhex("0400000005040101"),
                "Start Project Ack", [1, 4, 1, 1, 2]
            )
        elif choice == "6":
            simulate_inbound_event(
                bytes.fromhex("0500000006040102"),
                "Ack/Retry Response", [1, 4, 1, 1, 2]
            )
        elif choice == "7":
            print("Exiting node simulator.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    run_node_simulator()