# node_pps_manager.py
import time
import RPi.GPIO as GPIO

PPS_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PPS_PIN, GPIO.IN)

pps_epoch = None

def wait_for_pps():
    global pps_epoch
    GPIO.wait_for_edge(PPS_PIN, GPIO.RISING)
    pps_epoch = time.time()
    return pps_epoch

def get_seconds_since_midnight():
    global pps_epoch
    if pps_epoch is None:
        return None
    t = time.gmtime(pps_epoch)
    return t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec