# node_sht31_driver.py
import adafruit_sht31d
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
sht31 = adafruit_sht31d.SHT31D(i2c)

def read_sht31():
    try:
        temperature = sht31.temperature
        humidity = sht31.relative_humidity
        return {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2)
        }
    except Exception as e:
        return {"error": str(e)}