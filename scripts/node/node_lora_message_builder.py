# node_lora_message_builder.py

from utils.protocol import encode_message  # Assumes protocol handles encoding into bytes

class OutboundMessageBuilder:
    def build(self, event_dict):
        try:
            return encode_message(event_dict)
        except Exception as e:
            print(f"[OutboundBuilder] Encoding failed: {e}")
            return None
