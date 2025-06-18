# node_sensor_message_packer.py

from node.node_weather_sampler import sample_weather
from node.node_telemetry import process_telemetry
from birdnet_edit import get_mock_birdnet_detection  # currently returns random detection

class SensorMessage:
    def __init__(self, sensor_type, content, target=None):
        self.sensor_type = sensor_type
        self.content = content
        self.target = target

    def to_dict(self):
        result = {
            "sensor_type": self.sensor_type,
            "data": self.content
        }
        if self.target:
            result["target"] = self.target
        return result


class SensorMessagePacker:
    @staticmethod
    def build_weather():
        content = sample_weather()
        return SensorMessage("weather", content, target="send_over_lora")

    @staticmethod
    def build_telemetry():
        content = process_telemetry()
        return SensorMessage("telemetry", content, target="send_over_lora")

    @staticmethod
    def build_avis():
        content = get_mock_birdnet_detection()
        return SensorMessage("avis", content, target="send_over_lora")

