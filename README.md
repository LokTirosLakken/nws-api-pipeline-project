# NWS API Pipeline Project
This is a self-driven project to learn core concepts of data engineering.

## Current Progress
The first step is a Python script using the `requests` library to pull weather data from the National Weather Service API. It is designed to be called by a main script that passes in target coordinates.

### Usage: `get_forecast_by_coordinates(lat, long)`
* **Two arguments (`lat, long`):** Uses the provided latitude and longitude pair.
* **One argument (`lat`):** Uses the provided number as the latitude alongside the longitude for Austin, TX.
* **No arguments:** Defaults to the latitude and longitude pair for Austin, TX.
The latitude and longitude used for Austin, TX is (30.26715, -97.74306).

### Return Format
`get_forecast_by_coordinates()` returns a flattened dictionary in the following format:

```python
{
    "presentWeather": str,
    "temperature_celsius": float,
    "relative_humidity": float,
    "wind_speed_kilometer/hour": float,
    "barometric_pressure_Pascal": float,
    "visibility_meter": float,
    "observation_time": str  # ISO timestamp
}
```