# node_telemetry.py
from node.node_hardware_manager import collect_sensor_data
from node.node_altitude_calibrator import (
    calibrate_altitude
)
from node.node_gps_calibrator import (
    calibrate_coordinates
)

def process_telemetry():
    """Collects all sensor readings and returns calibrated telemetry."""

    data = collect_sensor_data()
    gps_result = calibrate_coordinates()
    alt_result = calibrate_altitude()

    telemetry = {
        "temperature_sht": data.get("sht31", {}).get("temperature"),
        "humidity": data.get("sht31", {}).get("humidity"),
        "temperature_bmp": alt_result.get("temperature") if alt_result else None,
        "pressure": alt_result.get("pressure") if alt_result else None,
        "calibrated_altitude_baro": alt_result.get("altitude") if alt_result else None,
        "calibrated_altitude_gps": gps_result.get("alt") if gps_result else None,
        "latitude": gps_result.get("lat") if gps_result else None,
        "longitude": gps_result.get("lon") if gps_result else None,
        "hdop": gps_result.get("hdop") if gps_result else None,
        "fix_type": gps_result.get("fix_type") if gps_result else None,
        "num_satellites": gps_result.get("num_satellites") if gps_result else None,
    }

    return telemetry
