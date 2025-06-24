# node_mode_manager.py

from node.node_initial_launch import InitialLaunch

class ModeManager:
    def __init__(self):
        self.mode = "Avis Lite"  # Default mode
        self.launcher = InitialLaunch()

    def update_mode(self, inbound_payload):
        try:
            new_mode = inbound_payload.get("content", {}).get("mode")
            if new_mode:
                print(f"[ModeManager] Switching mode from {self.mode} → {new_mode}")
                self.mode = new_mode
            else:
                print("[ModeManager] No mode specified in payload.")
        except Exception as e:
            print(f"[ModeManager] Mode change failed: {e}")

    def initialize(self, inbound_payload):
        print("[ModeManager] Launching node initialization...")
        self.launcher.run(inbound_payload)

    def get_current_mode(self):
        return self.mode

