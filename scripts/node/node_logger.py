# node_logger.py

import os
from datetime import datetime

class Logger:
    def __init__(self, log_dir=None):
        # Default to a “logs” folder alongside your scripts
        base = os.path.abspath(os.path.dirname(__file__))
        self.log_dir = log_dir or os.path.join(base, "../logs")
        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, event_obj):
        """Log a structured event object in plain text format."""
        try:
            date_str = datetime.utcnow().strftime("%Y-%m-%d")
            file_path = os.path.join(self.log_dir, f"log_{date_str}.txt")
            log_entry = self.format_entry(event_obj)

            with open(file_path, "a") as f:
                f.write(log_entry + "\n")

        except Exception as e:
            print(f"[Logger] Failed to write log: {e}")

    def format_entry(self, event_obj):
        """Format an event object into a clear, human-readable string."""
        try:
            obj = event_obj.to_dict()
        except Exception:
            return "[Logger] Invalid event object, could not serialize."

        timestamp = obj.get("timestamp", "unknown_time")
        event_type = obj.get("event_type", "unknown_event")
        node_id = obj.get("node_id", "unknown_node")
        uid = obj.get("uid", "no_uid")
        summary = f"[{timestamp}] {event_type.upper()} from Node {node_id} | UID: {uid}"

        # Optional debug details (useful in simulators)
        extra = " | ".join(
            f"{k}: {v}" for k, v in obj.items()
            if k not in {"timestamp", "event_type", "node_id", "uid"}
        )

        return f"{summary} | {extra}" if extra else summary
