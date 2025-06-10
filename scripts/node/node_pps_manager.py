# node_pps_manager.py
import time

try:
    import RPi.GPIO as GPIO
    IS_PI = True
except ImportError:
    GPIO = None
    IS_PI = False

PPS_PIN = 18
pps_epoch = None

def setup_gpio():
    if IS_PI:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PPS_PIN, GPIO.IN)

def wait_for_pps():
    global pps_epoch

    if not IS_PI:
        print("[PPS] Simulator mode: faking PPS signal")
        pps_epoch = time.time()
        return pps_epoch

    GPIO.wait_for_edge(PPS_PIN, GPIO.RISING)
    pps_epoch = time.time()
    return pps_epoch

def get_seconds_since_midnight():
    global pps_epoch

    if pps_epoch is None:
        # Simulate a default PPS time if not available
        return 43200  # noon

    t = time.gmtime(pps_epoch)
    return t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec
