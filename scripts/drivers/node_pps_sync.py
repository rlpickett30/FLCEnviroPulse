# node_pps_sync.py
import RPi.GPIO as GPIO
import time

PPS_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PPS_PIN, GPIO.IN)

last_pps_time = None

def wait_for_pps():
    global last_pps_time
    GPIO.wait_for_edge(PPS_PIN, GPIO.RISING)
    last_pps_time = time.time()
    return last_pps_time

def get_last_pps():
    return last_pps_time
