# lora_simulator.py

class LoraSimulator:
    def __init__(self):
        self.sample_messages = [
            b'\x01\x0A\x1F\xC3',
            b'\x02\x1B\xFF\x99',
            b'\x03\x0D\xAA\xEE'
        ]
        self.index = 0

    def get_next_message(self):
        if self.index < len(self.sample_messages):
            msg = self.sample_messages[self.index]
            self.index += 1
            return msg
        return None  # No new messages
