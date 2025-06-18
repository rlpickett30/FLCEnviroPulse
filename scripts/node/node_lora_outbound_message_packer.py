# node_lora_outbound_message_packer.py

from utils.protocol import Protocol
from node.node_send_over_lora import LoRaSender

class OutboundMessageBuilder:
    def __init__(self):
        self.protocol = Protocol(map_directory="config/maps")
        self.sender = LoRaSender()

    def build(self, event_dict):
        """
        Encodes an event_dict into a binary payload using protocol structure.
        """
        try:
            return self.protocol.encode(event_dict)
        except Exception as e:
            print(f"[OutboundBuilder] Encoding failed: {e}")
            return None

    def send(self, event_obj):
        """
        Performs the full outbound operation:
        - Generates UID
        - Encodes with protocol
        - Stores for retry
        - Sends via LoRa (or simulates)
        """
        try:
            self.sender.send(event_obj)
        except Exception as e:
            print(f"[OutboundBuilder] Send failed: {e}")
