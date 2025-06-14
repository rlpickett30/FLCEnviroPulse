# node_ack_manager.py

from node.node_unique_id_manager import acknowledge_event

def handle_ack(ack_payload):
    acked_uid = ack_payload["uid"]
    acknowledge_event(acked_uid)

class AckManager:
    def build_response(self, event_obj):
        try:
            inbound = event_obj.inbound
            original_event_id = inbound["header"].get("event_id")

            return {
                "header": {
                    "event_id": "ACK",
                    "timestamp": self._get_current_time(),
                    "response_to": original_event_id
                },
                "content": {
                    "node_id": inbound["content"]["node_id"]
                }
            }
        except Exception as e:
            print(f"[AckManager] Failed to build ACK: {e}")
            return None

    def _get_current_time(self):
        from time import time
        return int(time())
