# node_lora_message_builder.py

from utils.protocol import Protocol

class OutboundMessageBuilder:
    def __init__(self):
        self.protocol = Protocol(map_directory="config/maps")

    def build(self, event_dict):
        try:
            return self.protocol.encode(event_dict)
        except Exception as e:
            print(f"[OutboundBuilder] Encoding failed: {e}")
            return None
