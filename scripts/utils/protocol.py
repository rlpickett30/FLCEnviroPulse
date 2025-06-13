import json
from pathlib import Path

# --- Map Loader with Reversal ---
class MapManager:
    def __init__(self, map_directory: str):
        root = Path(__file__).resolve().parents[2]
        self.map_directory = (root / map_directory).resolve()
        self.maps = {}

    def load_map(self, name: str):
        # Always try with “.json” extension
        filename = name if name.endswith(".json") else f"{name}.json"
        path = self.map_directory / filename
        if not path.exists():
            raise FileNotFoundError(f"Map file not found: {path}")

        forward_map = json.loads(path.read_text())
        # Build reverse map with integer keys
        reverse_map = {int(v): k for k, v in forward_map.items()}

        self.maps[name] = {"forward": forward_map, "reverse": reverse_map}
        return self.maps[name]

    def get_forward(self, map_name: str, key):
        forward = self.load_map(map_name)["forward"]
        return forward.get(key)  # key should be the label string

    def get_reverse(self, map_name: str, value: int):
        reverse = self.load_map(map_name)["reverse"]
        return reverse.get(value)  # lookup with the int code directly

# --- Message Protocol Handling ---
class Protocol:
    def __init__(self, map_directory: str):
        self.map_manager = MapManager(map_directory)

    # Core field‐lookup primitives
    def encode_field(self, map_name: str, label: str) -> int:
        """Convert human‐readable label to code."""
        code = self.map_manager.get_forward(map_name, label)
        if code is None:
            raise ValueError(f"Unknown label '{label}' in map '{map_name}'")
        return int(code)

    def decode_field(self, map_name: str, code: int) -> str:
        """Convert code to human‐readable label."""
        
        label = self.map_manager.get_reverse(map_name, code)
        if label is None:
            raise ValueError(f"Unknown code '{code}' in map '{map_name}'")
        return label


     # --- ACK / Retry / Fail ---
    def encode_ack_retry_type(self, label: str) -> int:
        return self.encode_field("ack_retry_map", label)

    def decode_ack_retry_type(self, code: int) -> str:
        return self.decode_field("ack_retry_map", code)

    # --- Confidence Scale ---
    def encode_confidence_level(self, description: str) -> int:
        return self.encode_field("confidence_scale_map", description)

    def decode_confidence_level(self, code: int) -> str:
        return self.decode_field("confidence_scale_map", code)

    # --- Event Type ---
    def encode_event_type(self, label: str) -> int:
        return self.encode_field("event_type_map", label)

    def decode_event_type(self, code: int) -> str:
        return self.decode_field("event_type_map", code)

    # --- Mode Type ---
    def encode_mode(self, label: str) -> int:
        return self.encode_field("mode_map", label)

    def decode_mode(self, code: int) -> str:
        return self.decode_field("mode_map", code)

    # --- Taxonomy (Bird Species) ---
    def encode_taxonomy(self, species_name: str) -> int:
        return self.encode_field("taxonomy_map", species_name)

    def decode_taxonomy(self, code: int) -> str:
        return self.decode_field("taxonomy_map", code)

    def decode(self, event_type: str, raw_payload: bytes) -> dict:
        """Decode a raw binary payload into structured data based on the event type."""
        import struct

        # Load structure_protocol.json
        base_dir = Path(__file__).resolve().parents[2]
        structure_path = base_dir / "config/structure_protocol/structure_protocol.json"
        with open(structure_path, "r") as f:
            structure = json.load(f)

        if event_type not in structure:
            raise ValueError(f"Unknown event type: {event_type}")

        spec = structure[event_type]
        fmt = spec["format"]
        fields = spec["fields"]

        # Decode using struct
        try:
            values = struct.unpack(fmt, raw_payload)
        except struct.error as e:
            raise ValueError(f"Struct unpacking failed: {e}")

        decoded = {}
        for field, val in zip(fields, values):
            name = field["name"]
            map_name = field.get("map")
            if map_name:
                decoded[name] = self.decode_field(map_name, val)
            else:
                decoded[name] = val

        return decoded
    
    
    def encode_with_uid(self, event_type: str, field_values: dict, uid: int) -> bytes:
        """
        Encode a full event into bytes, inserting the UID at the end.
        field_values should be a dict of all content fields except UID.
        """
        import struct, json

        # Load the structure
        root = Path(__file__).resolve().parents[2]
        structure = json.loads((root / "config/structure_protocol/structure_protocol.json").read_text())
        spec = structure[event_type]
        fmt = spec["format"]
        fields = spec["fields"]

        # Build the list of values in order
        values = []
        for field in fields:
            name = field["name"]
            if name == "uid":
                values.append(uid)
            else:
                val = field_values.get(name)
                # If there's a map, encode
                if "map" in field:
                    values.append(self.encode_field(field["map"].replace(".json",""), val))
                else:
                    values.append(val)
        # Pack
        return struct.pack(fmt, *values)
