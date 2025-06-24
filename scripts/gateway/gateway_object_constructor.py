from gateway.gateway_heading_wrapper import HeadingWrapper

"""
Wraps decoded inbound events from LoRa or server into a complete gateway object,
attaching a gateway timestamp and collecting UIDs from node/server headers.
"""

class GatewayEventConstructor:
    def __init__(self):
        self.wrapper = HeadingWrapper()

    def construct(self, decoded_event):
        # Build base with gateway metadata (time + ID)
        base_wrapped = self.wrapper.build_base_event(decoded_event.get("raw_payload", b""))

        # Reattach node_header or server_header if present
        if "node_header" in decoded_event:
            base_wrapped["node_header"] = decoded_event["node_header"]
        if "server_header" in decoded_event:
            base_wrapped["server_header"] = decoded_event["server_header"]

        # Merge remaining core fields
        base_wrapped.update({
            "uid": decoded_event.get("uid"),
            "event_type": decoded_event.get("event_type"),
            "payload": decoded_event.get("payload", {}),
            "target": decoded_event.get("target", "unknown")
        })
        
        # Finalize gateway header with UID collection
        full_event = self.wrapper.attach_gateway_header(base_wrapped)
#        print("object_constructor")
#        print (full_event)
        return full_event

