# node_gps_driver.py

import time

try:
    import serial
    import adafruit_gps
    IS_PI = True
except ImportError:
    IS_PI = False

if IS_PI:
    uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
    gps = adafruit_gps.GPS(uart, debug=False)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")
else:
    gps = None

def read_gps():
    if not IS_PI or not gps:
        return {
            "fix": True,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "altitude_m": 1610.0,
            "timestamp": time.time()
        }

    gps.update()
    if not gps.has_fix:
        return {"fix": False, "message": "Waiting for fix"}

    return {
        "fix": True,
        "latitude": gps.latitude,
        "longitude": gps.longitude,
        "altitude_m": gps.altitude_m,
        "timestamp": time.time()
    }

