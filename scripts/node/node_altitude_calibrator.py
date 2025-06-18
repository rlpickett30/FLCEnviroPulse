# node_altitude_calibrator.py

import time
from statistics import mean
from node.node_bmp390_driver import read_bmp390

# Internal buffers for averaging
_alt_samples = []
_temp_samples = []
_pressure_samples = []

def pressure_to_altitude(pressure_hpa, sea_level_hpa=1013.25):
    """Converts pressure to altitude using the barometric formula."""
    return 44330.0 * (1.0 - (pressure_hpa / sea_level_hpa) ** (1.0 / 5.255))

def add_bmp_sample(sample):
    if not sample or "error" in sample:
        return
    pressure = sample["pressure"]
    temp = sample["temperature"]
    alt = pressure_to_altitude(pressure)
    
    _pressure_samples.append(pressure)
    _temp_samples.append(temp)
    _alt_samples.append(alt)

def calibrate_altitude(num_samples=10, delay_sec=1, offset=0.0):
    """Collects samples and returns averaged altitude, pressure, and temperature."""
    for _ in range(num_samples):
        sample = read_bmp390()
        add_bmp_sample(sample)
        time.sleep(delay_sec)

    if not _alt_samples:
        return None

    avg_alt = round(mean(_alt_samples) + offset, 2)
    avg_temp = round(mean(_temp_samples), 2)
    avg_pressure = round(mean(_pressure_samples), 2)

    return {
        "altitude": avg_alt,
        "temperature": avg_temp,
        "pressure": avg_pressure,
        "method": "bmp_averaged"
    }