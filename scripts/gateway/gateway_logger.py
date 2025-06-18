# gateway_logger.py

import json
import os
from datetime import datetime

BASE_LOG_DIR = "logs"


def log_event(event):
    try:
        # Determine filename
        event_type = event.get("event_type", "unknown")
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        log_dir = os.path.join(BASE_LOG_DIR, date_str)
        os.makedirs(log_dir, exist_ok=True)

        file_path = os.path.join(log_dir, f"{event_type}.jsonl")

        # Write event as one JSON line
        with open(file_path, 'a') as f:
            f.write(json.dumps(event) + "\n")

    except Exception as e:
        print(f"[LOGGER ERROR] Could not log event: {e}")

