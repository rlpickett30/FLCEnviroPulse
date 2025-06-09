# node_hardware_manager.py
from utils.node_sht31_driver import read_sht31
from utils.node_bmp390_driver import read_bmp390
from utils.node_gps_driver import read_gps
from utils.node_pps_sync import get_last_pps

def collect_sensor_data():
    data = {
        "sht31": read_sht31(),
        "bmp390": read_bmp390(),
        "gps": read_gps(),
        "pps_time": get_last_pps()
    }
    return data

def collect_environmental_packet():
    raw = collect_sensor_data()
    # Flatten or reformat as needed for dispatch
    return {
        "temperature_sht": raw.get("sht31", {}).get("temperature"),
        "humidity": raw.get("sht31", {}).get("humidity"),
        "temperature_bmp": raw.get("bmp390", {}).get("temperature"),
        "pressure": raw.get("bmp390", {}).get("pressure"),
        "latitude": raw.get("gps", {}).get("latitude"),
        "longitude": raw.get("gps", {}).get("longitude"),
        "altitude_m": raw.get("gps", {}).get("altitude_m"),
        "gps_fix": raw.get("gps", {}).get("fix"),
        "pps_time": raw.get("pps_time")
    }