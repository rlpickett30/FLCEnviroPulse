# node_sensor_message_packer.py

from node.node_weather_sampler import sample_weather
from node.node_telemetry import process_telemetry
from birdnet_edit import get_mock_birdnet_detection  # currently returns random detection

class SensorMessage:
    def __init__(self, sensor_type, content):
        self.sensor_type = sensor_type  # e.g., "weather", "telemetry", "avis"
        self.content = content

    def to_dict(self):
        return {
            "sensor_type": self.sensor_type,
            "data": self.content
        }

class SensorMessagePacker:
    @staticmethod
    def build_weather():
        content = sample_weather()
        return SensorMessage("weather", content)

    @staticmethod
    def build_telemetry():
        content = process_telemetry()
        return SensorMessage("telemetry", content)

    @staticmethod
    def build_avis():
        # If you later want to pass args like taxonomy_id or confidence, update get_mock_birdnet_detection
        content = get_mock_birdnet_detection()
        return SensorMessage("avis", content)
