# gateway_registry_manager.py

import json
import os


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GATEWAY_REGISTRY_PATH = os.path.join(ROOT_DIR, "config", "registers", "gateway_registry.json")

class GatewayRegistryManager:
    def __init__(self, registry_path=GATEWAY_REGISTRY_PATH):
        self.registry_path = registry_path
        self.registry = self.load_registry()

    def load_registry(self):
        if not os.path.exists(self.registry_path):
            raise FileNotFoundError(f"Gateway registry not found at {self.registry_path}")
        with open(self.registry_path, 'r') as file:
            return json.load(file)

    def get(self, key):
        return self.registry.get(key)

    def update(self, key, value):
        self.registry[key] = value
        self.save_registry()

    def get_all(self):
        return self.registry

    def save_registry(self):
        with open(self.registry_path, 'w') as file:
            json.dump(self.registry, file, indent=2)

    def __str__(self):
        return json.dumps(self.registry, indent=2)


# Example usage (for testing):
if __name__ == "__main__":
    manager = GatewayRegistryManager()
    print("Current Gateway Info:")
    print(manager)
