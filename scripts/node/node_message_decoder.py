# node_message_decoder.py

from utils.protocol import decode_message
from node.node_sanity_check import SanityChecker


class MessageDecoder:
    def __init__(self):
        self.sanity_checker = SanityChecker()

    def decode_and_validate(self, raw_payload):
        try:
            structured_message = decode_message(raw_payload)
        except Exception as e:
            raise ValueError(f"Decoding failed: {e}")

        if not self.sanity_checker.validate(structured_message):
            raise ValueError("Sanity check failed")

        return structured_message
