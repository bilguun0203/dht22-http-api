# DHT22 Simple HTTP API

## Dependencies

**System:**

```sh
sudo apt install libgpiod2
```

**Python:**


```sh
pip3 install -r requirements.txt
```

## Endpoint

### Get measurement

`GET /read`

**Response:**

```json
{
    "t": 20.0,
    "h": 40.0
}
```

- `t` - Temperature (Celsius)
- `h` - Humidity (%)
