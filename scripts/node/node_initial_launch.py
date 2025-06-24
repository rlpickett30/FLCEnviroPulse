#initial_launch.py

from node.node_time import get_timestamp
from node.node_registries_manager import load_registry, get_firmware_version, get_model_index, get_taxonomy_version

class InitialLaunch:
    def __init__(self, obj):
        self.obj = obj

    def handle(self):
        try:
            content = self.obj.payload.get("content", {})
            node_id = content.get("node_id")
            project_name = content.get("project_name")
            enclosure_id = content.get("enclosure_id")
            uid = self.obj.payload.get("uid")
            timestamp = self.obj.payload.get("timestamp") or get_timestamp()

            # Update registry
            load_registry({
                "node_id": node_id,
                "project_name": project_name,
                "enclosure_id": enclosure_id,
                "uid": uid
            })

            # Insert firmware, model, and taxonomy into the object before re-dispatch
            self.obj.payload.update({
                "timestamp": timestamp,
                "node_id": node_id,
                "model": get_model_index(),
                "firmware": get_firmware_version(),
                "version": get_taxonomy_version(),
                "uid": uid
            })

            return self.obj

        except Exception as e:
            print(f"[InitialLaunch] Error during initialization: {e}")
            return None


