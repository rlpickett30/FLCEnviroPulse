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
    class MockGPS:
        def __init__(self):
            self.samples = [
                {"lat": 37.7519, "lon": -107.6814, "alt": 2034.8, "hdop": 0.9},
                {"lat": 37.7520, "lon": -107.6815, "alt": 2035.2, "hdop": 0.8},
                {"lat": 37.7521, "lon": -107.6813, "alt": 2035.5, "hdop": 0.7},
                {"lat": 37.7518, "lon": -107.6816, "alt": 2034.7, "hdop": 1.0},
                {"lat": 37.7517, "lon": -107.6812, "alt": 2035.1, "hdop": 0.9},
                {"lat": 37.7520, "lon": -107.6814, "alt": 2035.0, "hdop": 0.8},
                {"lat": 37.7522, "lon": -107.6815, "alt": 2035.4, "hdop": 0.7},
                {"lat": 37.7519, "lon": -107.6816, "alt": 2034.9, "hdop": 0.8},
                {"lat": 37.7521, "lon": -107.6813, "alt": 2035.3, "hdop": 0.9},
                {"lat": 37.7520, "lon": -107.6812, "alt": 2035.2, "hdop": 0.8}
            ]
            self.index = 0
            self.has_fix = True

        def update(self):
            self.index = (self.index + 1) % len(self.samples)

        @property
        def latitude(self):
            return self.samples[self.index]["lat"]

        @property
        def longitude(self):
            return self.samples[self.index]["lon"]

        @property
        def altitude_m(self):
            return self.samples[self.index]["alt"]

    gps = MockGPS()

def read_gps():
    gps.update()

    if not gps.has_fix:
        return { "fix": False, "message": "Waiting for fix" }

    return {
        "fix": True,
        "Latitude": gps.latitude,
        "Longitude": gps.longitude,
        "altitude_m": gps.altitude_m,
        "timestamp": time.time()
    }
