import json
import os
from datetime import datetime

BASE_LOG_DIR = "logs"

class GatewayLogger:
    """
    Handles all persistent logging of gateway-handled events.
    Events routed here via target='push_to_server'.
    """

    def __init__(self):
        pass

    def get_target(self):
        return "push_to_server"

    def log_event(self, event, stage="UNKNOWN"):
        try:
            event_to_log = self._sanitize_for_logging(event)

            event_type = event_to_log.get("event_type", "unknown")
            date_str = datetime.utcnow().strftime("%Y-%m-%d")
            log_dir = os.path.join(BASE_LOG_DIR, date_str)
            os.makedirs(log_dir, exist_ok=True)

            file_path = os.path.join(log_dir, f"{event_type}.jsonl")
            with open(file_path, 'a') as f:
                f.write(json.dumps(event_to_log, sort_keys=True) + "\n")

            print(f"[{stage}] Event logged: {event_type}")

        except Exception as e:
            print(f"[LOGGER ERROR] Could not log event: {e}")


    def _sanitize_for_logging(self, event):
        clean = dict(event)

        # Remove or convert raw_payload
        if "raw_payload" in clean:
            try:
                clean["raw_payload"] = clean["raw_payload"].hex()
            except Exception:
                clean.pop("raw_payload")
        return clean

