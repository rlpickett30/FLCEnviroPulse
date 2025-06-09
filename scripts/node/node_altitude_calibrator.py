# node_altitude_calibrator.py
from statistics import mean

altitude_samples = []
pressure_samples = []

# This module adjusts raw BMP390 or GPS altitude readings based on a known offset
# or uses a pressure-based reference sea-level conversion.

def add_altitude_sample(sample):
    if sample is not None:
        altitude_samples.append(sample)

def add_pressure_sample(sample):
    if sample is not None:
        pressure_samples.append(sample)

def calibrate_altitude(offset=0.0):
    if not altitude_samples:
        return None
    avg_alt = mean(altitude_samples)
    return round(avg_alt + offset, 2)

def calibrate_pressure_to_altitude(sea_level_pressure_hpa=1013.25):
    if not pressure_samples:
        return None
    avg_pressure = mean(pressure_samples)
    altitude = 44330 * (1.0 - (avg_pressure / sea_level_pressure_hpa) ** (1.0 / 5.255))
    return round(altitude, 2)
