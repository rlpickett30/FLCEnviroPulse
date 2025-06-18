# gateway_object_constructor.py

from gateway.gateway_base_object import build_base_event, ensure_uid

"""
This module merges inbound LoRa or server events with a base event structure.
The base event attaches a gateway header and ensures UID assignment where missing.

Expected input:
- decoded_event: an object from lora or server builder (dict with node_header + payload)

Returns:
- fully constructed event with gateway header and complete node_header
"""

def construct_gateway_event(decoded_event):
    # Wrap it with base gateway header and raw payload preserved
    base_wrapped = build_base_event(decoded_event.get("raw_payload", b''))

    # Transfer other headers/payload into the base wrapper
    base_wrapped.update({
        "node_header": decoded_event.get("node_header", {}),
        "event_type": decoded_event.get("event_type"),
        "payload": decoded_event.get("payload", {})
    })

    # Ensure UID is attached
    full_event = ensure_uid(base_wrapped)

    return full_event


# Example usage
if __name__ == "__main__":
    # Simulated decoded inbound object
    fake_decoded = {
        "node_header": {
            "node_id": 3,
            "node_time": 12345678
        },
        "event_type": "telemetry",
        "payload": {"temperature": 18, "humidity": 30},
        "raw_payload": b"\x03\x00..."  # Optional binary
    }

    event = construct_gateway_event(fake_decoded)
    from pprint import pprint
    pprint(event)
