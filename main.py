import os
import time
from datetime import datetime

import adafruit_dht
import board
import uvicorn
from fastapi import FastAPI

host = os.getenv("HOST", "127.0.0.1")
port = os.getenv("PORT", 5000)

app = FastAPI()


def measure():
    dht22 = None
    try:
        dht22 = adafruit_dht.DHT22(board.D4, use_pulseio=True)
        temperature = dht22.temperature
        humidity = dht22.humidity
        dht22.exit()
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
        if dht22 is not None:
            dht22.exit()
    return None, None


@app.get("/read")
def read():
    humid, temp = measure()
    if humid is None or temp is None:
        # if failed, try measure once more
        time.sleep(1)
        humid, temp = measure()
    return {"h": humid, "t": temp}


if __name__ == "__main__":
    port = int(port)
    print(f"Starting server on {host}:{port}. ")
    uvicorn.run("main:app", host=host, port=port, log_level="info")
