# node_bmp390_driver.py

try:
    import adafruit_bmp3xx
    import board
    import busio
    IS_PI = True
except ImportError:
    IS_PI = False

if IS_PI:
    i2c = busio.I2C(board.SCL, board.SDA)
    bmp390 = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    bmp390.pressure_oversampling = 8
    bmp390.temperature_oversampling = 2
else:
    class MockBMP390:
        def __init__(self):
            self.samples = [
                {"temperature": 20.9, "pressure": 1012.6},
                {"temperature": 21.2, "pressure": 1012.8},
                {"temperature": 21.0, "pressure": 1013.0},
                {"temperature": 21.3, "pressure": 1012.9},
                {"temperature": 21.1, "pressure": 1012.7},
                {"temperature": 21.4, "pressure": 1012.6},
                {"temperature": 21.2, "pressure": 1012.8},
                {"temperature": 21.0, "pressure": 1013.1},
                {"temperature": 21.3, "pressure": 1012.9},
                {"temperature": 21.1, "pressure": 1012.7}
            ]
            self.index = 0

        def update(self):
            self.index = (self.index + 1) % len(self.samples)

        def read(self):
            self.update()
            return self.samples[self.index]

    bmp390 = MockBMP390()

def read_bmp390():
    if not IS_PI or not bmp390:
        return bmp390.read()

    try:
        temperature = bmp390.temperature
        pressure = bmp390.pressure
        return {
            "temperature": round(temperature, 2),
            "pressure": round(pressure, 2)
        }
    except Exception as e:
        return {"error": str(e)}

