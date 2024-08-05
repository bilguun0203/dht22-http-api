import Adafruit_DHT
import time
import uvicorn
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()


def read_sensor():
    dht22 = Adafruit_DHT.DHT22
    try:
        humidity, temperature = Adafruit_DHT.read_retry(dht22, 4)
        humidity = None if humidity > 100 else humidity
        if humidity is not None and temperature is not None:
            print(
                datetime.now(),
                "Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity),
            )
        else:
            print(datetime.now(), "Failed to retrieve data from humidity sensor")
        return humidity, temperature
    except Exception as e:
        print(datetime.now(), f"Error: {e}")
    return None, None


@app.get("/read")
def dht22():
    humid, temp = read_sensor()
    return {"h": humid, "t": temp}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
