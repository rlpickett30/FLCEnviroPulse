# node_sht31_driver.py

try:
    import adafruit_sht31d
    import board
    import busio
    IS_PI = True
except ImportError:
    IS_PI = False
    adafruit_sht31d = None
    board = None
    busio = None

if IS_PI:
    i2c = busio.I2C(board.SCL, board.SDA)
    sht31 = adafruit_sht31d.SHT31D(i2c)
else:
    sht31 = None  # simulation mode

def read_sht31():
    if not IS_PI or not sht31:
        return {
            "temperature": 22.5,  # Simulated °C
            "humidity": 42.0      # Simulated %RH
        }

    try:
        temperature = sht31.temperature
        humidity = sht31.relative_humidity
        return {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2)
        }
    except Exception as e:
        return {"error": str(e)}
