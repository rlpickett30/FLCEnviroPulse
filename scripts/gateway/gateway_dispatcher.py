# gateway_dispatcher.py

from gateway.gateway_ack_retry_manager import store_event
# from transmit import transmit_over_lora  # placeholder
# from gateway_logger import log_event  # coming next

"""
This dispatcher receives any fully constructed event and routes it:
- Stores it in the retry manager if it should be acknowledged
- Logs the event to disk
- Sends it via LoRa if outbound

Assumes event already has:
- gateway_header
- node_header
- event_type
- payload
"""

def dispatch_event(event):
    uid = event["node_header"]["uid"]
    event_type = event.get("event_type")

    # Log the event (placeholder)
    log_event(event)

    # Track outbound events (ACK-needed)
    if is_ack_required(event_type):
        store_event(uid, event)

    # Transmit if needed
    if should_transmit(event_type):
        transmit_over_lora(event)

    print(f"[DISPATCHED] Event UID {uid} type: {event_type}")


def is_ack_required(event_type):
    # Define which events require ACK tracking
    return event_type in {"telemetry", "weather", "avis_lite", "avis_tdoa"}


def should_transmit(event_type):
    # Define which events trigger outbound sending
    return event_type in {"telemetry", "avis_lite", "avis_tdoa"}


def transmit_over_lora(event):
    # Placeholder: Replace with actual transmission function
    print(f"[SEND] Transmitting event UID {event['node_header']['uid']}")


def log_event(event):
    # Placeholder: Real logger will write to file
    print(f"[LOG] Event UID {event['node_header']['uid']} logged.")
