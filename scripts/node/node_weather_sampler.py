# node_weather_sampler.py
from utils.node_hardware_manager import collect_sensor_data

def sample_weather():
    data = collect_sensor_data()
    weather = {
        "temperature": data.get("sht31", {}).get("temperature"),
        "humidity": data.get("sht31", {}).get("humidity"),
        "pressure": data.get("bmp390", {}).get("pressure")
    }
    return weather