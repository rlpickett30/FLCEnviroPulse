# node_constructor.py
from node.node_base_event import BaseEvent
from node.node_sensor_message_builder import SensorMessage

class ConstructedEvent:
    def __init__(self, event_type, sensor_obj=None, inbound_payload=None, category=None, target=None):
        self.base = BaseEvent(event_type)
        self.sensor = sensor_obj
        self.inbound = inbound_payload  # raw dict or parsed inbound message
        self.category = category
        self.target = target

    def to_dict(self):
        event = self.base.to_dict()

        if self.sensor:
            event["content"] = self.sensor.to_dict()
        elif self.inbound and "content" in self.inbound:
            event["content"] = self.inbound["content"]

        if self.inbound:
            event["inbound"] = self.inbound
        
        if self.category:
            event["category"] = self.category

        if self.target:
            event["target"] = self.target

        return event

