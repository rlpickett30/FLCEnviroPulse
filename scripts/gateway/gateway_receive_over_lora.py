# gateway_receive_over_lora.py

try:
    from drivers.rak2287_driver import receive_packet as receive_lora_packet
except ImportError:
    from tests.gateway_inbound_sim import receive_packet as receive_lora_packet

"""
This wrapper module ensures that the gateway can receive LoRa packets
using either the real RAK2287 hardware interface or a simulator fallback.

To use simulation mode, ensure `drivers.rak2287_driver` is unavailable or commented out,
and implement `receive_packet()` in `tests.gateway_inbound_sim.py`.

Usage:
    from gateway_receive_over_lora import receive_lora_packet
    data = receive_lora_packet()
"""
