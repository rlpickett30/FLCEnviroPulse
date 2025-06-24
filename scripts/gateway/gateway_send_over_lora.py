# gateway_send_over_lora.py

try:
    from drivers.rak2287_driver import send_packet as send_lora_packet
except ImportError:
    from tests.gateway_transmit_sim import send_packet as send_lora_packet

from gateway.gateway_lora_outbound_object_packer import build_lora_payload

class LoraOutboundSender:
    def __init__(self):
        pass

    def get_target(self):
        return "send_over_lora"

    def send(self, event):
        try:
            payload = build_lora_payload(event)
            send_lora_packet(payload)
            print(f"[LORA TX] Event UID {event['gateway_header']['uid']} sent.")
        except Exception as e:
            print(f"[LORA TX ERROR] {e}")
