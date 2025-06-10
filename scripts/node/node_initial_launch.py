# scripts/node/initial_launch.py

from node.node_lora_message_builder import OutboundMessageBuilder
from node.node_send_over_lora import LoRaSender
from node.node_registries_manager import get_node_id, get_firmware_version, load_registry

class InitialLauncher:
    def __init__(self):
        self.builder = OutboundMessageBuilder()
        self.sender = LoRaSender()

    def run(self, inbound_payload):
        try:
            # Pull device_uid (or other identifying info) from inbound
            node_info = inbound_payload.get("content", {})
            # If you need to persist or update the registry file:
            load_registry({"node_id": node_info.get("device_uid")})

            assigned_id = get_node_id()
            fw_version = get_firmware_version()

            launch_ack = {
                "header": {
                    "event_id": "Startup ACK",
                    "timestamp": self._get_current_time(),
                    "sender": "node",
                    "version": fw_version
                },
                "content": {
                    "node_id": assigned_id,
                    "status": "Initialized"
                }
            }

            encoded = self.builder.build(launch_ack)
            if encoded:
                self.sender.send(encoded)

        except Exception as e:
            print(f"[InitialLauncher] Initialization failed: {e}")

    def _get_current_time(self):
        from time import time
        return int(time())

