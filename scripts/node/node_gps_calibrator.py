# node_gps_calibrator.py

import time
from statistics import mean
from node.node_gps_driver import read_gps

# Internal sample lists
_lat_samples = []
_lon_samples = []
_alt_samples = []
_hdop_samples = []

def add_gps_sample(sample):
    if not sample.get("fix"):
        return
    _lat_samples.append(sample["Latitude"])
    _lon_samples.append(sample["Longitude"])
    _alt_samples.append(sample["altitude_m"])
    _hdop_samples.append(sample.get("hdop", 0.9))  # fallback if hdop missing

def calibrate_coordinates(lat_offset=0.0, lon_offset=0.0, alt_offset=0.0, num_samples=10, delay_sec=1):
    """Collects GPS samples and returns an averaged, corrected result."""

    for _ in range(num_samples):
        sample = read_gps()
        add_gps_sample(sample)
        time.sleep(delay_sec)

    if not _lat_samples or not _lon_samples:
        return None  # Calibration failed

    avg_lat = round(mean(_lat_samples) + lat_offset, 6)
    avg_lon = round(mean(_lon_samples) + lon_offset, 6)
    avg_alt = round(mean(_alt_samples) + alt_offset, 1)
    avg_hdop = round(mean(_hdop_samples), 2)

    return {
        "lat": avg_lat,
        "lon": avg_lon,
        "alt": avg_alt,
        "hdop": avg_hdop,
        "fix_type": 3,  # Mock or define if using actual GPS enum
        "num_satellites": 8,  # You can update to track this too if needed
        "method": "averaged"
    }
