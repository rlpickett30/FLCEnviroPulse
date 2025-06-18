# gateway_send_over_lora.py

try:
    from drivers.rak2287_driver import send_packet as send_lora_packet
except ImportError:
    # Fallback to simulation mode if hardware driver not available
    from tests.gateway_transmit_sim import send_packet as send_lora_packet

from gateway.gateway_lora_outbound_object_builder import build_lora_payload

"""
This module finalizes outbound events by:
- Encoding them into binary packets
- Transmitting via RAK2287 or simulator
"""

def send_event_over_lora(event):
    try:
        payload = build_lora_payload(event)
        send_lora_packet(payload)
        print(f"[LORA TX] Event UID {event['node_header']['uid']} sent.")
    except Exception as e:
        print(f"[LORA TX ERROR] {e}")


