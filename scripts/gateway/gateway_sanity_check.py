# gateway_sanity_check.py

def sanity_check(event):
    required_top_level = ["event_type"]

    for key in required_top_level:
        if key not in event:
            print(f"[SANITY CHECK] Missing required key: {key}")
            return False

    # Event-specific checks
    if event["event_type"] in ["telemetry", "weather", "startup_ack"]:
        if "payload" not in event:
            print("[SANITY CHECK] Missing required key: payload")
            return False

    return True
