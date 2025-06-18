# gateway_server_simulator.py

import time
from utils.protocol import Protocol
from gateway.gateway_base_object import build_base_event
from gateway.gateway_object_constructor import construct_gateway_event
from gateway.gateway_server_inbound_object_builder import build_server_event
from gateway.gateway_lora_outbound_object_builder import build_lora_payload
from gateway.gateway_send_over_lora import send_lora_packet

"""
Simulates server-originated events, testing full object formation:
- Adds base gateway header
- Constructs complete node event
- Encodes to binary
- Sends over LoRa
- Displays detailed debugging
"""

protocol = Protocol("config/maps")

def split_hex_chunks(hex_str, field_lengths):
    chunks = []
    i = 0
    for byte_len in field_lengths:
        chunks.append(hex_str[i:i + (byte_len * 2)])
        i += (byte_len * 2)
    return chunks

def print_debug(event, encoded, field_lengths):
    hex_str = encoded.hex()
    chunks = split_hex_chunks(hex_str, field_lengths)

    print("\n[RAW]:", hex_str)
    print("[DELIM]:", " | ".join(chunks))
    print("[TRANS]:")
    print(f"  Type:      {event['event_type']}")
    print(f"  UID:       {event['node_header']['uid']}")
    print(f"  Node ID:   {event['node_header'].get('node_id', 'N/A')}")
    print(f"  Payload:   {event['payload']}")
    print(f"  Gateway ID: {event['gateway_header'].get('gateway_id', 'N/A')}")
    print(f"  Gateway Time: {event['gateway_header'].get('gateway_time', 'N/A')}")


def simulate_event(raw_event, field_lengths):
    base = build_base_event(None)  # Create gateway header
    decoded = build_server_event(raw_event)  # Add node + payload
    decoded["gateway_header"] = base["gateway_header"]  # Apply base header
    wrapped = construct_gateway_event(decoded)
    encoded = build_lora_payload(wrapped)
    print_debug(wrapped, encoded, field_lengths)
    send_lora_packet(encoded)


def run_server_simulator():
    while True:
        print("\n[SERVER SIM MENU]")
        print("1. Simulate Start Project")
        print("2. Simulate Change Mode")
        print("3. Simulate Recalibrate Node")
        print("4. Quit")

        choice = input("Choose simulation: ").strip()

        if choice == "1":
            raw = {
                "event_type": "start_project",
                "project_name": "Sim_Animas",
                "mode": "avis_lite",
                "timestamp": int(time.time()),
                "node_list": [1, 2]
            }
            print("[WARN] start_project not encoded to LoRa — routed for pipeline test only.")
            simulate_event(raw, [1, 4, 1, 1, 4])

        elif choice == "2":
            raw = {
                "event_type": "change_mode",
                "node_id": 3,
                "mode": "telemetry",
                "timestamp": int(time.time())
            }
            simulate_event(raw, [1, 4, 1, 1, 4])

        elif choice == "3":
            raw = {
                "event_type": "change_mode",
                "node_id": 2,
                "mode": "recalibrate",
                "timestamp": int(time.time())
            }

            print("[WARN] recalibrate_node not implemented for outbound LoRa encoding.")
            simulate_event(raw, [1, 4, 1, 1, 4])

        elif choice == "4":
            print("Exiting server simulator.")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    run_server_simulator()
