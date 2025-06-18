# gateway_server_inbound_listener.py

import json
import time
from pathlib import Path

from gateway_server_inbound_object_builder import build_server_event
from gateway_object_constructor import construct_gateway_event

"""
Simulates listening to the server by reading JSON-formatted events from a file.
Each event is processed, tagged with a gateway header, and passed along for dispatch/logging.

When your partner returns, replace the input with a socket, REST, or message queue.
"""

SIMULATED_INPUT_PATH = "tests/simulated_server_input.json"


def listen_for_server_events():
    input_path = Path(SIMULATED_INPUT_PATH)
    if not input_path.exists():
        raise FileNotFoundError(f"No simulated input found at {SIMULATED_INPUT_PATH}")

    with open(input_path, 'r') as f:
        try:
            events = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse input JSON: {e}")

    for raw_event in events:
        try:
            decoded = build_server_event(raw_event)
            wrapped = construct_gateway_event(decoded)
            dispatch_server_event(wrapped)
        except Exception as e:
            print(f"Error handling server event: {e}")
        time.sleep(1)  # Optional: space out simulated arrival


def dispatch_server_event(event):
    # Placeholder: Route to logs, dispatcher, etc.
    print("\n[Server Event Dispatched]")
    from pprint import pprint
    pprint(event)


if __name__ == "__main__":
    listen_for_server_events()
