# node_pps_sync.py

import time

try:
    import RPi.GPIO as GPIO
    IS_PI = True
except ImportError:
    GPIO = None
    IS_PI = False

PPS_PIN = 18
last_pps_time = None

def setup_gpio():
    if IS_PI:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PPS_PIN, GPIO.IN)

def wait_for_pps():
    global last_pps_time
    if not IS_PI:
        print("[PPS] Simulated PPS pulse")
        last_pps_time = time.time()
        return last_pps_time

    GPIO.wait_for_edge(PPS_PIN, GPIO.RISING)
    last_pps_time = time.time()
    return last_pps_time

def get_last_pps():
    return last_pps_time if last_pps_time else time.time()
