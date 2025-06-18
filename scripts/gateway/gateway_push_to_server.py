# gateway_push_to_server.py

import json
import os
from datetime import datetime

SERVER_LOG_DIR = "server_received"


def receive_event(event):
    # Display the decoded node-level message
    print("\n[SERVER RECEIVED]")
    print(f"Event Type  : {event.get('event_type')}")
    print(f"Node Header : {event.get('node_header')}")
    print(f"Payload     : {event.get('payload')}")

    # Archive copy to JSONL
    save_event_to_server_log(event)


def save_event_to_server_log(event):
    try:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        os.makedirs(SERVER_LOG_DIR, exist_ok=True)
        file_path = os.path.join(SERVER_LOG_DIR, f"{date_str}.jsonl")

        with open(file_path, 'a') as f:
            f.write(json.dumps(event) + "\n")

    except Exception as e:
        print(f"[SERVER LOG ERROR] {e}")

