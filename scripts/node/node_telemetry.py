# node_telemetry.py
from node.node_hardware_manager import collect_sensor_data
from node.node_altitude_calibrator import add_altitude_sample, add_pressure_sample, calibrate_altitude, calibrate_pressure_to_altitude
from node.node_gps_calibrator import add_gps_sample, calibrate_coordinates


def process_telemetry():
    data = collect_sensor_data()

    gps = data.get("gps", {})
    bmp = data.get("bmp390", {})

    # Feed raw readings into calibrators
    add_altitude_sample(gps.get("altitude_m"))
    add_pressure_sample(bmp.get("pressure"))
    add_gps_sample(gps.get("latitude"), gps.get("longitude"))

    # Create telemetry event dict
    telemetry = {
        "temperature_sht": data.get("sht31", {}).get("temperature"),
        "humidity": data.get("sht31", {}).get("humidity"),
        "temperature_bmp": bmp.get("temperature"),
        "pressure": bmp.get("pressure"),
        "calibrated_altitude_gps": calibrate_altitude(),
        "calibrated_altitude_baro": calibrate_pressure_to_altitude(),
        "latitude": None,
        "longitude": None,
    }

    lat, lon = calibrate_coordinates()
    telemetry["latitude"] = lat
    telemetry["longitude"] = lon

    return telemetry