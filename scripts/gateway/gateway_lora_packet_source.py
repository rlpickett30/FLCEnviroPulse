# gateway_lora_packet_source.py



import os
from drivers.gateway_rak2287_driver import receive_packet as receive_hardware_packet
from gateway.gateway_lora_inbound_object_packer import decode_wrapped_packet
from gateway.gateway_dispatcher import dispatch_event as dispatch_gateway
from gateway.gateway_logger import GatewayLogger
from datetime import datetime

logger = GatewayLogger()

# Simulated packet queue
_simulated_packet_queue = []

def inject_simulated_packet(data: bytes):
    _simulated_packet_queue.append(data)
    print(f"[SIMULATION] Packet injected: {data.hex()}")

def receive_packet():
    use_sim = os.getenv("ENVIRPULSE_SIMULATION_MODE", "false").lower() == "true"
    print(f"[SIMULATION] Simulation Mode = {use_sim}")

    if use_sim:
        if _simulated_packet_queue:
            packet = _simulated_packet_queue.pop(0)

        
            print(f"[SIMULATION] Packet dequeued: {packet.hex()}")
            print(f"[LOOP] Raw packet received: {packet.hex()}")

            # ⬇️ Route directly to inbound packer
            wrapped = {
                "gateway_header": {
                    "uid": "gateway_01",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                "raw_payload": packet
            }

            decoded_event = decode_wrapped_packet(wrapped)
            logger.log_event(decoded_event, stage="LORA INPUT")
            dispatch_gateway(decoded_event)

            return None  # Skip listener's normal decode flow
        else:
            return None
    else:
        return receive_hardware_packet()
