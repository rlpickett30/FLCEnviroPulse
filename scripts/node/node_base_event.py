# node_base_event.py
import uuid
from node.node_time import get_timestamp
from node.node_registries_manager import get_node_id, get_firmware_version

class BaseEvent:
    def __init__(self, event_type, sensor_obj=None):
        self.event_id = self._generate_event_id()
        self.timestamp = get_timestamp()
        self.sender = get_node_id()
        self.version = get_firmware_version()
        self.event_type = event_type
        self.sensor_obj = sensor_obj  # Optional SensorMessage object

    def _generate_event_id(self):
        return str(uuid.uuid4())

    def attach_sensor_data(self, sensor_obj):
        self.sensor_obj = sensor_obj

    def to_dict(self):
        base = {
            "header": {
                "event_id": self.event_id,
                "timestamp": self.timestamp,
                "sender": self.sender,
                "version": self.version
            },
            "event_type": self.event_type
        }
        if self.sensor_obj:
            base["content"] = self.sensor_obj.to_dict()
        return base