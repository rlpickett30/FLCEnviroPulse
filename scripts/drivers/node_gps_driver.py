# node_gps_driver.py
import time
import serial
import adafruit_gps

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")  # 1Hz update rate

def read_gps():
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