# NWS API Pipeline Project
This is a self-driven project to learn core concepts of data engineering.

## Limitations
-On November 17, 2026, the NWS latest-observation endpoint returned HTTP 503 during testing, so the end-to-end pipeline could not complete. The request currently surfaces this as a JSON parsing error; clearer handling of API errors is planned.

## Current Progress
We now have a main script that can perform an API request to fetch observation data from NWS, validate them and load them into a database.

#### Problems to tackle:
- NWS's API had an outage, but my code did not read for an HTML status code and returned confusing errors. This needs to be updated.
- Add tests for various input types
- Coordinate validation
- Updating documentation

#### Future plans
-Make this automated through Github Actions
-Coordinate validation for custom coordinates
-Custom database file (might need this for Github Actions?)
-Free cloud database



## Usage
From the repository root, install the dependencies and run the pipeline:

```shell
python -m pip install -r requirements.txt
python src/nws_api_main.py
```

The script fetches the latest observation for Austin, Texas, cleans the values, and inserts the observation into `weather_data.db`.

To call the fetch function directly:

```python
from src.nws_api_helper_functions import get_forecast_by_coordinates

# Defaults to Austin, Texas.
observation = get_forecast_by_coordinates()

# Pass latitude and longitude in decimal degrees for another location.
observation = get_forecast_by_coordinates(37.7749, -122.4194)
```

The function signature is `get_forecast_by_coordinates(lat=30.26715, lon=-97.74306)`. If only `lat` is supplied, the longitude defaults to Austin's longitude.

The returned dictionary contains:

```python
{
    "present_weather": "Clear",
    "temperature_celsius": 22.5,
    "relative_humidity": 50.0,
    "wind_speed_kilometer_hour": 12.0,
    "barometric_pressure_Pascal": 101325.0,
    "visibility_meters": 16000.0,
    "observation_time": "2026-11-17T15:00:00+00:00",
    "time_recorded": "2026-11-17T15:01:00+00:00",
    "station_id": "KATT"
}
```

Numeric measurements may be `None` when the station does not report a value. `clean_observation_data()` rounds numeric measurements to two decimal places.