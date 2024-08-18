import os
import time
from datetime import datetime
from functools import lru_cache

import adafruit_dht
import board
import uvicorn
from fastapi import Depends, FastAPI, Response
from typing_extensions import Annotated

host = os.getenv("HOST", "127.0.0.1")
port = os.getenv("PORT", 5000)

app = FastAPI()


@lru_cache
def get_dht22():
    return adafruit_dht.DHT22(board.D4, use_pulseio=True)


def measure(dht22):
    try:
        temperature = dht22.temperature
        humidity = dht22.humidity
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
def read(dht22: Annotated[adafruit_dht.DHT22, Depends(get_dht22)], response: Response):
    humid, temp = measure(dht22)
    if humid is None or temp is None:
        # if failed, try measure once more
        time.sleep(1)
        humid, temp = measure(dht22)
    if humid is None or temp is None:
        response.status_code = 500
    return {"h": humid, "t": temp}


if __name__ == "__main__":
    port = int(port)
    print(f"Starting server on {host}:{port}. ")
    uvicorn.run("main:app", host=host, port=port, log_level="info")
