# node_registries_manager.py
import json
import os

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), 'registries.json')

REGISTRY = {
    "node_id": 0,
    "firmware_version": "0.0.0",
    "event_type_map": {},
    "taxonomy_map": {},
    "nodes": []
}

# Load registries.json at runtime
if os.path.exists(REGISTRY_PATH):
    with open(REGISTRY_PATH, 'r') as f:
        try:
            data = json.load(f)
            REGISTRY.update(data)
        except json.JSONDecodeError:
            print("Error: Could not parse registries.json")


def get_node_id():
    return REGISTRY.get("node_id", 0)

def get_firmware_version():
    return REGISTRY.get("firmware_version", "0.0.0")

def get_event_code(event_type):
    return REGISTRY.get("event_type_map", {}).get(event_type, -1)

def get_taxonomy_code(label):
    return REGISTRY.get("taxonomy_map", {}).get(label, -1)

def get_node_registry(index=0):
    try:
        return REGISTRY["nodes"][index]
    except (IndexError, KeyError):
        return {}

def get_all_node_registries():
    return REGISTRY.get("nodes", [])

def load_registry(new_dict):
    REGISTRY.update(new_dict)

def get_registry():
    return REGISTRY

def get_model_index(model_label=None):
    """Return integer code for model, defaulting to first node if not provided."""
    model_label = model_label or get_node_registry().get("node_type", "")
    return REGISTRY.get("model_map", {}).get(model_label, -1)

def get_taxonomy_version(label=None):
    """Return integer code for taxonomy label."""
    label = label or get_node_registry().get("taxonomy_version", "")
    return REGISTRY.get("taxonomy_map", {}).get(label, -1)

def get_uid():
    """Return current node UID, if assigned."""
    return get_node_registry().get("uid", 0)