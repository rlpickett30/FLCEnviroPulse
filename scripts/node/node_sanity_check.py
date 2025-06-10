# node_sanity_check.py

class SanityChecker:
    def __init__(self):
        # Define required fields and constraints
        self.required_keys = ['event_id', 'timestamp', 'sender', 'version']

    def validate(self, message):
        if not isinstance(message, dict):
            return False

        for key in self.required_keys:
            if key not in message.get("header", {}):
                return False

        # Example: Check timestamp is non-negative integer
        if not isinstance(message["header"]["timestamp"], int) or message["header"]["timestamp"] < 0:
            return False

        return True
