# node_inbound_message_builder.py

from node.node_constructor import ConstructedEvent


class InboundBuilder:
    def __init__(self):
        self.supported_event_types = {
            "ack_retry_event",
            "change_mode",
            "init",
            "telemetry_event",
            "weather_event",
            "avis_event"
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
            
            if event_type == "ack_retry_event":
                return ConstructedEvent(
                    event_type=event_type,
                    inbound_payload=decoded_inbound,
                    category="system",
                    target="ack_handler"
                )    
            
            if event_type == "change_mode":
                return ConstructedEvent(
                    event_type=event_type,
                    inbound_payload=decoded_inbound,
                    category="command",
                    target="mode_manager"
                )
            
            if event_type == "init":
                return ConstructedEvent(
                    event_type=event_type,
                    inbound_payload=decoded_inbound,
                    category="handshake",
                    target="launch_manager"
                )
            
            if event_type == "telemetry_event":
                return ConstructedEvent(
                    event_type=event_type,
                    inbound_payload=decoded_inbound,
                    category="data",
                    target="telemetry_logger"
                )
            
            if event_type == "weather_event":
                return ConstructedEvent(
                    event_type=event_type,
                    inbound_payload=decoded_inbound,
                    category="data",
                    target="weather_logger"
                )
            
            if event_type == "avis_event":
                return ConstructedEvent(
                    event_type=event_type,
                    inbound_payload=decoded_inbound,
                    category="data",
                    target="avis_logger"
                )


        except Exception as e:
            print(f"[InboundBuilder] Failed to build event: {e}")
            return None
