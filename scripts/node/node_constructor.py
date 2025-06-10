# node_constructor.py
from node.node_base_event import BaseEvent
from node.node_sensor_message_builder import SensorMessage

class ConstructedEvent:
    def __init__(self, event_type, sensor_obj=None, inbound_payload=None):
        self.base = BaseEvent(event_type)
        self.sensor = sensor_obj
        self.inbound = inbound_payload  # raw dict or parsed inbound message

    def to_dict(self):
        event = self.base.to_dict()
        if self.sensor:
            event["content"] = self.sensor.to_dict()
        if self.inbound:
            event["inbound"] = self.inbound
        return event