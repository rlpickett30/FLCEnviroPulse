# gateway_lora_outbound_object_builder.py

from utils.protocol import Protocol

# Init Protocol
protocol = Protocol("config/maps")

# Only supported outbound encodable messages
ENCODABLE_EVENTS = {
    "ack_retry_event",
    "telemetry_event",
    "change_mode",
    "startup_ack",
    "start_project"
}

def build_lora_payload(event):
    event_type_str = event["event_type"]

    if event_type_str not in ENCODABLE_EVENTS:
        raise ValueError(f"[ENCODE ERROR] Unsupported event type: {event_type_str}")

    # Encode event type into integer after validation
    event_type = protocol.encode_event_type(event_type_str)

    field_values = {
        "event_type": event_type,
    }

    # Try node_header first, else fallback
    node_header = event.get("node_header", {})
    if "node_id" in node_header:
        field_values["node_id"] = node_header["node_id"]
    if "node_time" in node_header:
        field_values["node_time"] = node_header["node_time"]

    # Pull UID
    uid = node_header.get("uid", event.get("uid"))

    # Add payload fields
    field_values.update(event.get("payload", {}))

    # Encode
    encoded = protocol.encode_with_uid(event_type_str, field_values, uid)
    return encoded
