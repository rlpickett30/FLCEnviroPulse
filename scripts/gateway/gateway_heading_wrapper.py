import time
from gateway.gateway_registry_manager import GatewayRegistryManager

"""
This class-based wrapper ensures each event gets a consistent gateway header.
It collects existing unique identifiers from the node and server, but does not generate them.
"""

class HeadingWrapper:
    def __init__(self):
        self.registry = GatewayRegistryManager()

    def build_base_event(self, raw_payload):
        return {
            "gateway_header": {
                "gateway_time": time.gmtime(time.time()),
                "gateway_id": self.registry.get("gateway_id")
            },
            "raw_payload": raw_payload
        }

    def attach_gateway_header(self, event_obj):
        gateway_header = {
            "gateway_time": time.gmtime(time.time()),
            "gateway_id": self.registry.get("gateway_id"),
            }

    # Grab the first available UID
        uid = (
            event_obj.get("server_header", {}).get("uid")
            or event_obj.get("node_header", {}).get("uid")
    )

        gateway_header["uid"] = uid
        event_obj["gateway_header"] = gateway_header
        return event_obj

