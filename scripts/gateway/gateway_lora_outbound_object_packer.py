# gateway_lora_outbound_object_packer.py

from utils.protocol import Protocol
from pprint import pprint

# Init Protocol
protocol = Protocol("config/maps")

# Only supported outbound encodable messages
ENCODABLE_EVENTS = {
    "ack_retry_event",
    "change_mode",
    "start_project",
    "recalibrate"
}

def build_lora_payload(event):
    event_type_str = event["event_type"]    
    gateway_header = event.get("gateway_header", {})

    if event_type_str not in ENCODABLE_EVENTS:
        raise ValueError(f"[ENCODE ERROR] Unsupported event type: {event_type_str}")
    
    # Encode event type into integer after validation
    event_type = protocol.encode_event_type(event_type_str)
    field_values = {
        "event_type": event_type,
    }
    
    if event.get("event_type") == "change_mode":
        mode = event.get("payload", {}).get("mode")
        if mode is not None:
            field_values["mode"] = mode
            
    # Optionally include gateway metadata
    if "gateway_id" in gateway_header:
        field_values["gateway_id"] = gateway_header["gateway_id"]
    if "gateway_time" in gateway_header:
        field_values["gateway_time"] = gateway_header["gateway_time"]

    # Extract UID (always from gateway_header now)
    uid = gateway_header.get("uid")

    # Debugging output before encoding
#    print("[DEBUG] Final field_values passed to encoder:")
#    pprint(field_values)
#    print(f"[DEBUG] UID: {uid}")

    # Encode
    encoded = protocol.encode_with_uid(event_type_str, field_values, uid)
    return encoded

