# node_gps_calibrator.py
from statistics import mean

latitude_samples = []
longitude_samples = []

# This module applies any user-defined adjustments to GPS coordinates.

def add_gps_sample(lat, lon):
    if lat is not None and lon is not None:
        latitude_samples.append(lat)
        longitude_samples.append(lon)

def calibrate_coordinates(lat_offset=0.0, lon_offset=0.0):
    if not latitude_samples or not longitude_samples:
        return (None, None)
    avg_lat = mean(latitude_samples)
    avg_lon = mean(longitude_samples)
    corrected_lat = round(avg_lat + lat_offset, 6)
    corrected_lon = round(avg_lon + lon_offset, 6)
    return (corrected_lat, corrected_lon)