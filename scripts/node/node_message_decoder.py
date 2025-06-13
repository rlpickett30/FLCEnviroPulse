# node_message_decoder.py

# node_message_decoder.py

from utils.protocol import Protocol
from node.node_sanity_check import SanityChecker

class MessageDecoder:
    def __init__(self):
        self.sanity_checker = SanityChecker()
        self.protocol = Protocol(map_directory="config/maps")

    def decode_and_validate(self, raw_payload):
        try:
            # Step 1: Extract event_type code
            event_code = raw_payload[0]

            # Step 2: Map code → event_type name
            event_type = self.protocol.decode_event_type(event_code)

            # Step 3: Decode full message
            structured = self.protocol.decode(event_type, raw_payload)

            # Step 4: Build envelope for sanity check
            envelope = {
                "header": {
                    "event_id": event_type,
                    "timestamp": structured["timestamp"],
                    "sender": "simulator",
                    "version": "v0.1"
                },
                "content": {k: v for k, v in structured.items() if k != "timestamp"}
            }

        except Exception as e:
            raise ValueError(f"Decoding failed: {e}")

        # Single sanity‐check pass
        if not self.sanity_checker.validate(envelope):
            raise ValueError("Sanity check failed")

        return envelope
