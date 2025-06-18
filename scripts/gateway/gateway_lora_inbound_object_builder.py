# gateway_lora_inbound_object_builder.py

from utils.protocol import Protocol
from gateway.gateway_sanity_check import sanity_check

"""
This module receives wrapped gateway packets, performs structure validation,
and decodes their contents using the protocol module.
If decoding fails, an error object is returned for downstream handling.
"""

# Initialize Protocol object
protocol = Protocol("config/maps")

def decode_wrapped_packet(wrapped_packet):
    try:
        raw = wrapped_packet.get("raw_payload")
        gateway_header = wrapped_packet.get("gateway_header")

        # Peek at event_type (first byte or known location) to decode
        event_type_code = raw[0]
        event_type = protocol.decode_event_type(event_type_code)

        decoded = protocol.decode(event_type, raw)
        print("[DEBUG] Event Type:", decoded.get("event_type"))
        print("[DEBUG] Available Keys:", list(decoded.keys()))
        if not sanity_check(decoded):
            raise ValueError("Sanity check failed")

        decoded_event = {
            "gateway_header": gateway_header,
            "node_header": {
                "node_id": decoded["node_id"],
                "node_time": decoded["node_time"],
                "uid": decoded["uid"]
            },
            "event_type": event_type,
            "payload": {k: v for k, v in decoded.items()
                         if k not in ("node_id", "node_time", "uid")}
        }
        return decoded_event
        
        

    except Exception as e:
        print("[DEBUG] Decode failure:", e)
        return {
            "gateway_header": wrapped_packet.get("gateway_header"),
            "event_type": "error",
            "error": str(e),
            "raw_payload": wrapped_packet.get("raw_payload")
        }
