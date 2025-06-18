import node_pps_manager as pps_manager
from node_base_event import BaseEvent

def simulate_pps_base_event():
    print("\n[SIM] Starting PPS-driven base event test...")

    # Step 1: Simulate PPS pulse (uses real modules)
    pps_time = pps_manager.wait_for_pps()

    # Step 2: Get timestamp based on PPS epoch
    timestamp = pps_manager.get_seconds_since_midnight()

    print(f"[SIM] PPS epoch: {pps_time}")
    print(f"[SIM] Derived timestamp: {timestamp}")

    # Step 3: Build a dummy base event
    base = BaseEvent(
        event_type="test_event",
        timestamp=timestamp,
        node_id=1,
        uid=12345
    )

    print(f"[SIM] Constructed BaseEvent: {base}")