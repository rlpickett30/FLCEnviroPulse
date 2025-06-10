# scripts/node/node_logger.py

import json
import os
from datetime import datetime

class Logger:
    def __init__(self, log_dir=None):
        # Default to a “logs” folder alongside your scripts
        base = os.path.abspath(os.path.dirname(__file__))
        self.log_dir = log_dir or os.path.join(base, "../logs")
        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, event_obj):
        try:
            # ISO date for filename, UTC
            date_str = datetime.utcnow().strftime("%Y-%m-%d")
            file_path = os.path.join(self.log_dir, f"log_{date_str}.jsonl")
            with open(file_path, "a") as f:
                f.write(json.dumps(event_obj.to_dict()) + "\n")
        except Exception as e:
            print(f"[Logger] Failed to write log: {e}")
