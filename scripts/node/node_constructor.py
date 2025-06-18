# node_constructor.py

from node.node_heading_wrapper import BaseEvent
from node.node_sensor_message_packer import SensorMessage
from node.node_lora_inbound_message_packer import InboundBuilder

class ConstructedEvent:
    def __init__(self, event_type, sensor_obj=None, lora_inbound=None, category=None, target=None):
        """
        Creates a structured event object, wrapping either node-generated or LoRa-inbound content.

        Args:
            event_type (str): Canonical event type string (e.g., "telemetry_event")
            sensor_obj (SensorMessage, optional): Sensor object from message packer
            lora_inbound (dict, optional): Validated and decoded LoRa input
            category (str, optional): System category label (e.g., "data", "command")
            target (str, optional): Handler identifier (e.g., "telemetry_logger")
        """
        self.header = BaseEvent(event_type, sensor_obj)
        self.sensor = sensor_obj
        self.lora_inbound = lora_inbound
        self.category = category
        self.target = target

    def to_dict(self):
        event = self.header.to_dict()

        if self.sensor:
            event["content"] = self.sensor.to_dict()
        elif self.lora_inbound and "content" in self.lora_inbound:
            event["content"] = self.lora_inbound["content"]

        if self.lora_inbound:
            event["lora_inbound"] = self.lora_inbound

        if self.category:
            event["category"] = self.category

        if self.target:
            event["target"] = self.target

        return event
