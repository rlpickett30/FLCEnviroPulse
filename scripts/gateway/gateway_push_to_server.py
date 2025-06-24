# gateway_push_to_server.py

import json
import os
from datetime import datetime

SERVER_LOG_DIR = "server_received"

class ServerReceiver:
    def __init__(self):
        self.handlers = {
            "avis_tdoa": self.handle_avis_tdoa,
            "weather": self.handle_weather,
            "avis_lite": self.handle_avis_lite,
            "telemetry": self.handle_telemetry,
            "startup_ack": self.handle_startup_ack,
        }

    def receive_event(self, event):
        event_type = event.get("event_type", "unknown")

        print("\n[SERVER RECEIVED]")
        print(f"Event Type  : {event_type}")
        print(f"Node Header : {event.get('node_header')}")
        print(f"Payload     : {event.get('payload')}")

        # Dispatch to the appropriate handler
        handler = self.handlers.get(event_type, self.handle_unknown)
        handler(event)

        # Always archive
        self._save_event_to_server_log(event)

    def handle_avis_tdoa(self, event):
        # Placeholder for future TDOA logic
        pass

    def handle_weather(self, event):
        # Placeholder for future weather ingestion
        pass

    def handle_avis_lite(self, event):
        # Placeholder for fast-track lite processing
        pass

    def handle_telemetry(self, event):
        # Placeholder for internal health monitoring
        pass

    def handle_startup_ack(self, event):
        # Placeholder for handshake or registry sync
        pass

    def handle_unknown(self, event):
        print(f"[WARNING] Unknown event type: {event.get('event_type')}")

    def get_target(self):
        return "push_to_server"


    def _save_event_to_server_log(self, event):
        try:
            date_str = datetime.utcnow().strftime("%Y-%m-%d")
            os.makedirs(SERVER_LOG_DIR, exist_ok=True)
            file_path = os.path.join(SERVER_LOG_DIR, f"{date_str}.jsonl")

            with open(file_path, 'a') as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            print(f"[SERVER LOG ERROR] {e}")
