#Purpose: 
#A helper file that takes care of SQL functions such as building and loading the database

import sqlite3



#Function to create table connection and table if not found, otherwise does nothing
def create_table(connection):


    #We also need to create a cursor object to execute SQL commands.
    cursor = connection.cursor()

    SQL_initializing_statement = """CREATE TABLE IF NOT EXISTS weather_data(
        present_weather TEXT,
        temperature_celsius REAL,
        relative_humidity REAL,
        wind_speed_kilometer_hour REAL,
        barometric_pressure_Pascal REAL,
        visibility_meters REAL,
        observation_time TEXT NOT NULL,
        time_recorded TEXT NOT NULL,
        station_id TEXT NOT NULL,
        PRIMARY KEY (station_id,observation_time))"""

    # create a database connection
    try:
        cursor.execute(SQL_initializing_statement)

        # commit the changes
        connection.commit()

        print("Tables created successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to create tables:", e)

#End of create_table()

#Function to insert weather observation data into the table
#Input:
#   connection: SQLite3 database connection
#   observation: dictionary of weather values
#Output: Nothing is returned. The result is an attempt at a new entry in the database and committing it.
def insert_observation(connection, observation):
    cursor = connection.cursor()#Converts dictionary into an array of results
    values = (observation["present_weather"],
        observation["temperature_celsius"],
        observation["relative_humidity"],
        observation["wind_speed_kilometer_hour"],
        observation["barometric_pressure_Pascal"],
        observation["visibility_meters"],
        observation["observation_time"],
        observation["time_recorded"],
        observation["station_id"])
    #Performs SQL INSERT operation using array of results from before.
    #Idempotency:
    #   Composite key on station_id and observation_time
    #   Any attempt to add a record with a duplicate station_id and observation_time is rejected 
    cursor.execute("""INSERT into weather_data(
        present_weather,
        temperature_celsius,
        relative_humidity,
        wind_speed_kilometer_hour,
        barometric_pressure_Pascal,
        visibility_meters,
        observation_time,
        time_recorded,
        station_id)
    VALUES (?,?,?,?,?,?,?,?,?)
    ON CONFLICT (station_id, observation_time) DO NOTHING
    """,
    values)

    connection.commit()
