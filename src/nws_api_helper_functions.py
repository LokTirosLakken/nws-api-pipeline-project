# %% [markdown]
# 11/8/26
# 
# Objective: Write a program that retrieves meteorlogical data for a coordinate pair and defaults to Austin, TX. It is structured to be imported and called by a script.
# 
# Input: 
# - Latitude and longitude pair.
# - If only one number is entered, it is used as the latitude, and Austin's longtitude is used.
# - If no numbers are entered, Austin's default coordinates are used: (30.26715, -97.74306).
# 
# 
# Output: A flattened dictionary consisting of meteorlogical data in the form:
#   "present_weather": string,
#   "temperature_celsius": float,
#   "relative_humidity": float,
# 	"wind_speed_kilometer_hour": float,
# 	"barometric_pressure_Pascal": float,
#   "visibility_meter": float,
#   "observation_time": string (ISO timestamp),
#   "time_recorded": string (iso timestamp)
#   "station_id": string,
# 
#  
#  Target API & Workflow (NWS API):
# 1. User-Agent Header: NWS requires a custom User-Agent string in the header (include a dummy/placeholder contact email).
# 2. Point Lookup: Make a GET request to https://api.weather.gov/points/{latitude},{longitude}
# 3. Station Lookup: Extract the URL from `properties > observationStations` in the JSON response.
# 4. Closest Station: Make a GET request to that URL and grab the first station ID in the list (the closest one).
# 5. Latest Observation: Request the latest data from https://api.weather.gov/stations/{stationId}/observations/latest
# 6. Flattening: Parse the resulting payload, extract the required metrics, and flatten them into the target output dictionary.
# 
# 
# Notes:
# Coordinates for Austin, TX are 30.26715, -97.74306 for latitude and longtitude respectively


# %%
import requests
from datetime import datetime, timezone
import math
import re




def get_forecast_by_coordinates(lat = 30.26715, lon = -97.74306): #Default coordinates are for Austin, TX

    HEADERS = {
    "User-Agent": "WeatherPipelineProject, A_random_mans_mail@gmail.com"}

    gridpoint_url = f"https://api.weather.gov/points/{lat},{lon}" #Builds the url for retrieving the gridpoint data



    try: #try block for retrieving the gridpoint data and station ID
        gridpoint_response = requests.get(gridpoint_url, headers=HEADERS)

        #fetch the URL for the observation stations from the gridpoint response JSON
        station_ID_url = gridpoint_response.json()['properties']['observationStations'] 

        #Navigate to the first station in the list, store its ID
        #Path is ['features']['0']['properties']['stationIdentifier']
        station_ID = requests.get(station_ID_url, headers=HEADERS).json()['features'][0]['properties']['stationIdentifier']

        #Build the URL for fetching current observations from the stations
        current_observations_url = f"https://api.weather.gov/stations/{station_ID}/observations/latest"

        #Fetch the current observations data by retrieving the properties dictionary from the JSON response
        current_observations_data = requests.get(current_observations_url, headers=HEADERS).json()['properties']

        #For this project, we just want the following fields:
        #temperature, relative humidity, wind speed, barometric pressure, and visibility
        #Also adding station ID to contribute to primary key
        flattened_properties = {
            "present_weather": current_observations_data['textDescription'],
            "temperature_celsius": current_observations_data['temperature']['value'],
            "relative_humidity": current_observations_data['relativeHumidity']['value'],
            "wind_speed_kilometer_hour": current_observations_data['windSpeed']['value'],
            "barometric_pressure_Pascal": current_observations_data['barometricPressure']['value'],
            "visibility_meters": current_observations_data['visibility']['value'],
            "observation_time": current_observations_data['timestamp'],
            "time_recorded": datetime.now(timezone.utc).isoformat(),
            "station_id": station_ID,
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching gridpoint data: {e}")
        raise



    #For testing:
    #print(current_observations_data)
    #print(f"The station ID is {station_ID}.")

    #Return the flattened dictionary of properties
    return flattened_properties
#end of get_forecast_by_coordinates


#%% NWS API Cleaner
# Purpose:
#   Accept a dictionary input and perform data validation on the entries within
#   This is logically separated from the ingestor to preserve raw data

def clean_observation_data(properties: dict):
    #Define some helper subfuntions
    def clean_float(value, precision = 2):
        #if numerical data is null or a boolean, set it to none, else cast it to float
        if value is None or isinstance(value, bool):
            return None
        try:
            num = float(value)
            if not math.isfinite(num):
                return None
            return round(num, precision)
        except (ValueError,TypeError): 
            return None
    #end of clean_float
    desc = properties.get("present_weather")
    cleaned_desc = desc.strip().capitalize() if isinstance(desc, str) and desc.strip else None

    station = properties.get("station_id")
    cleaned_station = station.strip().upper() if isinstance(station, str) and station.strip() else None

    return{
        "present_weather": cleaned_desc,
        "temperature_celsius": clean_float(properties.get("temperature_celsius")),
        "relative_humidity": clean_float(properties.get("relative_humidity")),
        "wind_speed_kilometer_hour": clean_float(properties.get("wind_speed_kilometer_hour")),
        "barometric_pressure_Pascal": clean_float(properties.get("barometric_pressure_Pascal")),
        "visibility_meters": clean_float(properties.get("visibility_meters")),
        "observation_time": properties.get("observation_time"),
        "time_recorded": properties.get("time_recorded"),
        "station_id": cleaned_station,        
    }

    

        
        

# %%Test
#raw_dict = get_forecast_by_coordinates()
#print(f"Raw dictionary is \n: {raw_dict}")
#print(f"Cleaned dictionary is \n: {clean_observation_data(raw_dict)}")
