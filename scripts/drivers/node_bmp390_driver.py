# node_bmp390_driver.py
import adafruit_bmp3xx
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
bmp390 = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp390.pressure_oversampling = 8
bmp390.temperature_oversampling = 2

def read_bmp390():
    try:
        temperature = bmp390.temperature
        pressure = bmp390.pressure
        return {
            "temperature": round(temperature, 2),
            "pressure": round(pressure, 2)
        }
    except Exception as e:
        return {"error": str(e)}
