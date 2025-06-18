# gateway_base_object.py

import time
from gateway.gateway_registry_manager import GatewayRegistryManager
from gateway.gateway_unique_id_manager import assign_uid

"""
Assigns gateway header and ensures UID exists if missing.
Should be called early in any gateway-originated or received message lifecycle.
"""

def build_base_event(raw_payload):
    registry = GatewayRegistryManager()
    return {
        "gateway_header": {
            "gateway_time": time.time(),
            "gateway_id": registry.get("gateway_id")
        },
        "raw_payload": raw_payload
    }

def ensure_uid(event_obj):
    if "node_header" not in event_obj:
        event_obj["node_header"] = {}

    if "uid" not in event_obj["node_header"] or event_obj["node_header"]["uid"] is None:
        assigned = assign_uid()
        event_obj["node_header"]["uid"] = assigned
        print(f"[UID Manager] Assigned UID {assigned} to event.")

    return event_obj