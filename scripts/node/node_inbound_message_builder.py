# node_inbound_message_builder.py

from node.node_constructor import ConstructedEvent


class InboundBuilder:
    def __init__(self):
        self.supported_event_types = {
            "ACK", "Retry", "Change Mode", "Error", "Init", "Telemetry", "Launch", "Update", "Fail"
        }

    def build(self, decoded_inbound):
        """
        Converts a decoded inbound message into a ConstructedEvent.

        Args:
            decoded_inbound (dict): A parsed LoRa message (already decoded).

        Returns:
            ConstructedEvent or None
        """
        try:
            event_type = decoded_inbound.get("header", {}).get("event_id", "")
            if event_type not in self.supported_event_types:
                raise ValueError(f"Unsupported inbound event: {event_type}")

            return ConstructedEvent(event_type=event_type, inbound_payload=decoded_inbound)

        except Exception as e:
            print(f"[InboundBuilder] Failed to build event: {e}")
            return None
