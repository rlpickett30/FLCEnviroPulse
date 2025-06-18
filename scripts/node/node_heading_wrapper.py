# node_heading_wrapper.py

from node.node_time import get_timestamp
from node.node_registries_manager import get_node_id, get_firmware_version
from node.node_unique_id_manager import UniqueIdManager

_uid_manager = UniqueIdManager()  # Could optionally pass a persistence path

class BaseEvent:
    def __init__(self, event_type, sensor_obj=None):
        self.uid = self._assign_uid()
        self.timestamp = self._safe_timestamp()
        self.sender = get_node_id()
        self.version = get_firmware_version()
        self.event_type = event_type
        self.sensor_obj = sensor_obj  # SensorMessage object (or None)

    def _assign_uid(self):
        return _uid_manager.next_id()

    def _safe_timestamp(self):
        try:
            return get_timestamp()
        except Exception as e:
            print(f"[WARN] Timestamp unavailable: {e}")
            return None

    def attach_sensor_data(self, sensor_obj):
        self.sensor_obj = sensor_obj

    def to_dict(self):
        base = {
            "header": {
                "uid": self.uid,
                "timestamp": self.timestamp,
                "sender": self.sender,
                "version": self.version
            },
            "event_type": self.event_type
        }
        if self.sensor_obj:
            base["content"] = self.sensor_obj.to_dict()
        return base
