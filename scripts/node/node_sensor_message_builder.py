# node_sensor_message_builder.py
from node.node_weather_sampler import sample_weather
from node.node_telemetry import process_telemetry
from birdnet_edit import generate_avis_event


class SensorMessage:
    def __init__(self, sensor_type, content):
        self.sensor_type = sensor_type  # e.g., "weather", "telemetry", "avis"
        self.content = content

    def to_dict(self):
        return {
            "sensor_type": self.sensor_type,
            "data": self.content
        }


class SensorMessageBuilder:
    @staticmethod
    def build_weather():
        content = sample_weather()
        return SensorMessage("weather", content)

    @staticmethod
    def build_telemetry():
        content = process_telemetry()
        return SensorMessage("telemetry", content)

    @staticmethod
    def build_avis(taxonomy_id, confidence, timestamp):
        content = generate_avis_event(taxonomy_id, confidence, timestamp)
        return SensorMessage("avis", content)
