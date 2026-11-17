# %% [markdown]
# Purpose
# 
# Write a main script for a NWS API project that builds a database by:
# 
#     Opening a database connection
#     using get_forecast_by_coordinates(lat,long) to ingest weather data
#     using clean_observation_data() to validate the data
#     Passing the connection into create_table to ensure weather_data.db exists by making one if it doesn't
#     Passing the connection and weather data dictionary into insert_observation to load the database
# 

# %%
import sqlite3
from nws_api_helper_functions import (
    get_forecast_by_coordinates,
    clean_observation_data,)
from database import(
    create_table,
    insert_observation
)


#                                             Main Logic Flow




#This forms a connection to the database file with the same name, or creates a new one if it doesn't exist
connection = sqlite3.connect('weather_data.db') 

#Gets observation data for Austin, TX   (Will work on data validation before adding input for other coordinates)
properties = get_forecast_by_coordinates()

#Validates data to ensure proper typing and format
cleaned_properties = clean_observation_data(properties)

#This function takes the database connection to make a new table if it doesn't exist, otherwise does nothing
create_table(connection)

#This function takes the database connection and cleaned observation data to insert it into the table
insert_observation(connection, cleaned_properties)




                                                #Testing
print(connection.execute("SELECT * FROM weather_data").fetchall())


#Closes connection, cuz that's just good business
connection.close()





