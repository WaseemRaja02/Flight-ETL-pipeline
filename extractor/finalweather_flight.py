import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone


# ============================================================
# API URLS
# ============================================================

AIRPORT_API = "https://pocketworld.org/api/airports"
FLIGHT_API = "https://pocketworld.org/api/flights"
OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"


# ============================================================
# SETTINGS
# ============================================================

MAX_WORKERS = 10
BATCH_SIZE = 100
TARGET_WEATHER = 1500


# ============================================================
# HELPER FUNCTION
# ============================================================

def extract_list(data, possible_keys):

    if isinstance(data, list):
        return data

    if isinstance(data, dict):

        for key in possible_keys:

            if isinstance(data.get(key), list):
                return data[key]

    return []


# ============================================================
# 1. GET AIRPORT DATA
# ============================================================

print("=" * 60)
print("GETTING AIRPORT DATA")
print("=" * 60)

try:

    response = requests.get(
        AIRPORT_API,
        timeout=30
    )

    response.raise_for_status()

    airport_json = response.json()

    airport_data = extract_list(
        airport_json,
        [
            "data",
            "airports",
            "results",
            "items"
        ]
    )

    df_airports = pd.json_normalize(
        airport_data
    )

    df_airports.to_csv(
        "airport_data.csv",
        index=False
    )

    print(
        "Airport rows:",
        len(df_airports)
    )

    print(
        "Airport columns:",
        len(df_airports.columns)
    )

except Exception as e:

    print(
        "Airport API error:",
        e
    )

    df_airports = pd.DataFrame()


# ============================================================
# 2. GET FLIGHT DATA
# ============================================================

print("\n")
print("=" * 60)
print("GETTING FLIGHT DATA")
print("=" * 60)

try:

    response = requests.get(
        FLIGHT_API,
        timeout=30
    )

    response.raise_for_status()

    flight_json = response.json()

    flight_data = extract_list(
        flight_json,
        [
            "data",
            "flights",
            "aircraft",
            "states",
            "results",
            "items"
        ]
    )

    df_flights = pd.json_normalize(
        flight_data
    )

    print(
        "Flight rows:",
        len(df_flights)
    )

    print(
        "Flight columns:",
        len(df_flights.columns)
    )

except Exception as e:

    print(
        "Flight API error:",
        e
    )

    df_flights = pd.DataFrame()


# ============================================================
# 3. FIND LATITUDE COLUMN
# ============================================================

lat_column = None

for column in [
    "lat",
    "latitude"
]:

    if column in df_flights.columns:

        lat_column = column
        break


if lat_column is None:

    raise Exception(
        "Latitude column not found in flight API."
    )


# ============================================================
# 4. FIND LONGITUDE COLUMN
# ============================================================

lon_column = None

for column in [
    "lng",
    "longitude",
    "lon"
]:

    if column in df_flights.columns:

        lon_column = column
        break


if lon_column is None:

    raise Exception(
        "Longitude column not found in flight API."
    )


# ============================================================
# 5. CREATE FLIGHT ID
# ============================================================

print("\nCreating flight IDs...")


def find_flight_id(row, index):

    possible_columns = [
        "flight_id",
        "id",
        "icao24",
        "icao",
        "aircraft_id"
    ]

    for column in possible_columns:

        if column in row.index:

            value = row[column]

            if pd.notna(value):

                value = str(value).strip()

                if value != "":
                    return value

    return f"FLIGHT_{index + 1}"


df_flights["flight_id"] = [

    find_flight_id(
        row,
        index
    )

    for index, row
    in df_flights.iterrows()

]


# ============================================================
# 6. CLEAN LATITUDE AND LONGITUDE
# ============================================================

print("\nCleaning coordinates...")

df_flights[lat_column] = pd.to_numeric(
    df_flights[lat_column],
    errors="coerce"
)

df_flights[lon_column] = pd.to_numeric(
    df_flights[lon_column],
    errors="coerce"
)


df_flights = df_flights.dropna(
    subset=[
        lat_column,
        lon_column
    ]
)


# ============================================================
# 7. REMOVE INVALID COORDINATES
# ============================================================

df_flights = df_flights[
    (
        df_flights[lat_column] >= -90
    )
    &
    (
        df_flights[lat_column] <= 90
    )
    &
    (
        df_flights[lon_column] >= -180
    )
    &
    (
        df_flights[lon_column] <= 180
    )
].copy()


# ============================================================
# 8. SAVE FLIGHT DATA
# ============================================================

df_flights.to_csv(
    "flight_data.csv",
    index=False
)

print(
    "Flight CSV created successfully."
)


# ============================================================
# 9. SELECT FLIGHT LOCATIONS
# ============================================================

print("\n")
print("=" * 60)
print("SELECTING FLIGHT WEATHER LOCATIONS")
print("=" * 60)


weather_locations = (

    df_flights[
        [
            "flight_id",
            lat_column,
            lon_column
        ]
    ]

    .dropna(
        subset=[
            lat_column,
            lon_column
        ]
    )

    .drop_duplicates(
        subset=[
            lat_column,
            lon_column
        ]
    )

    .reset_index(
        drop=True
    )

)


print(
    "Unique flight locations:",
    len(weather_locations)
)


# ============================================================
# 10. SELECT MAXIMUM 1500 LOCATIONS
# ============================================================

weather_locations = weather_locations.head(
    TARGET_WEATHER
)


print(
    "Weather locations selected:",
    len(weather_locations)
)


if len(weather_locations) == 0:

    raise Exception(
        "No valid flight locations found."
    )


# ============================================================
# 11. CREATE BATCHES
# ============================================================

batches = [

    weather_locations[
        start:start + BATCH_SIZE
    ]

    for start in range(
        0,
        len(weather_locations),
        BATCH_SIZE
    )

]


print(
    "Total Open-Meteo batches:",
    len(batches)
)


# ============================================================
# 12. OPEN-METEO WEATHER VARIABLES
# ============================================================

CURRENT_WEATHER_VARIABLES = [

    "temperature_2m",

    "relative_humidity_2m",

    "dew_point_2m",

    "apparent_temperature",

    "precipitation",

    "rain",

    "showers",

    "snowfall",

    "snow_depth",

    "weather_code",

    "cloud_cover",

    "pressure_msl",

    "surface_pressure",

    "visibility",

    "evapotranspiration",

    "vapour_pressure_deficit",

    "wind_speed_10m",

    "wind_direction_10m",

    "wind_gusts_10m",

    "uv_index",

    "uv_index_clear_sky",

    "is_day",

    "sunshine_duration",

    "cape",

    "freezing_level_height"

]


# ============================================================
# 13. GET WEATHER BATCH
# ============================================================

def get_weather_batch(batch):

    try:

        latitudes = batch[
            lat_column
        ].tolist()

        longitudes = batch[
            lon_column
        ].tolist()


        response = requests.get(

            OPEN_METEO_API,

            params={

                "latitude":
                    ",".join(
                        str(x)
                        for x in latitudes
                    ),

                "longitude":
                    ",".join(
                        str(x)
                        for x in longitudes
                    ),

                "current":
                    ",".join(
                        CURRENT_WEATHER_VARIABLES
                    ),

                "timezone":
                    "UTC"

            },

            timeout=120

        )


        response.raise_for_status()

        data = response.json()


        if not isinstance(
            data,
            list
        ):

            data = [data]


        results = []


        # ====================================================
        # MATCH WEATHER TO FLIGHT LOCATION
        # ====================================================

        for index, weather in enumerate(data):

            if index >= len(batch):
                continue


            row = batch.iloc[index]


            current = weather.get(
                "current",
                {}
            )


            results.append({

                # --------------------------------------------
                # FLIGHT INFORMATION
                # --------------------------------------------

                "flight_id":
                    row["flight_id"],

                "flight_latitude":
                    row[lat_column],

                "flight_longitude":
                    row[lon_column],


                # --------------------------------------------
                # WEATHER LOCATION
                # --------------------------------------------

                "weather_latitude":
                    weather.get(
                        "latitude"
                    ),

                "weather_longitude":
                    weather.get(
                        "longitude"
                    ),

                "weather_timezone":
                    weather.get(
                        "timezone"
                    ),

                "weather_elevation_m":
                    weather.get(
                        "elevation"
                    ),


                # --------------------------------------------
                # TEMPERATURE
                # --------------------------------------------

                "temperature_celsius":
                    current.get(
                        "temperature_2m"
                    ),

                "relative_humidity_percentage":
                    current.get(
                        "relative_humidity_2m"
                    ),

                "dew_point_celsius":
                    current.get(
                        "dew_point_2m"
                    ),

                "apparent_temperature_celsius":
                    current.get(
                        "apparent_temperature"
                    ),


                # --------------------------------------------
                # PRECIPITATION
                # --------------------------------------------

                "precipitation_mm":
                    current.get(
                        "precipitation"
                    ),

                "rain_mm":
                    current.get(
                        "rain"
                    ),

                "showers_mm":
                    current.get(
                        "showers"
                    ),

                "snowfall_cm":
                    current.get(
                        "snowfall"
                    ),

                "snow_depth_m":
                    current.get(
                        "snow_depth"
                    ),


                # --------------------------------------------
                # WEATHER CONDITION
                # --------------------------------------------

                "weather_code":
                    current.get(
                        "weather_code"
                    ),


                # --------------------------------------------
                # CLOUD / PRESSURE
                # --------------------------------------------

                "cloud_cover_percentage":
                    current.get(
                        "cloud_cover"
                    ),

                "pressure_msl_hpa":
                    current.get(
                        "pressure_msl"
                    ),

                "surface_pressure_hpa":
                    current.get(
                        "surface_pressure"
                    ),


                # --------------------------------------------
                # VISIBILITY / EVAPORATION
                # --------------------------------------------

                "visibility_m":
                    current.get(
                        "visibility"
                    ),

                "evapotranspiration_mm":
                    current.get(
                        "evapotranspiration"
                    ),

                "vapour_pressure_deficit_kpa":
                    current.get(
                        "vapour_pressure_deficit"
                    ),


                # --------------------------------------------
                # WIND
                # --------------------------------------------

                "wind_speed_kmh":
                    current.get(
                        "wind_speed_10m"
                    ),

                "wind_direction_degrees":
                    current.get(
                        "wind_direction_10m"
                    ),

                "wind_gusts_kmh":
                    current.get(
                        "wind_gusts_10m"
                    ),


                # --------------------------------------------
                # UV
                # --------------------------------------------

                "uv_index":
                    current.get(
                        "uv_index"
                    ),

                "uv_index_clear_sky":
                    current.get(
                        "uv_index_clear_sky"
                    ),


                # --------------------------------------------
                # DAY / SUN
                # --------------------------------------------

                "is_day":
                    current.get(
                        "is_day"
                    ),

                "sunshine_duration_seconds":
                    current.get(
                        "sunshine_duration"
                    ),


                # --------------------------------------------
                # ATMOSPHERIC / CONVECTIVE
                # --------------------------------------------

                "cape_jkg":
                    current.get(
                        "cape"
                    ),

                "freezing_level_height_m":
                    current.get(
                        "freezing_level_height"
                    ),


                # --------------------------------------------
                # WEATHER TIME
                # --------------------------------------------

                "weather_time_utc":
                    current.get(
                        "time"
                    ),


                # --------------------------------------------
                # INGESTION
                # --------------------------------------------

                "ingestion_timestamp_utc":
                    datetime.now(
                        timezone.utc
                    ).isoformat()

            })


        return results


    except Exception as e:

        print(
            "Batch error:",
            e
        )

        return []


# ============================================================
# 14. GET WEATHER IN PARALLEL
# ============================================================

print("\n")
print("=" * 60)
print("GETTING WEATHER DATA")
print("=" * 60)


weather_results = []


with ThreadPoolExecutor(
    max_workers=MAX_WORKERS
) as executor:


    futures = [

        executor.submit(
            get_weather_batch,
            batch
        )

        for batch in batches

    ]


    completed = 0


    for future in as_completed(
        futures
    ):

        completed += 1


        try:

            result = future.result()

            weather_results.extend(
                result
            )

        except Exception as e:

            print(
                "Weather batch error:",
                e
            )


        print(
            "Weather batches completed:",
            completed,
            "/",
            len(batches)
        )


# ============================================================
# 15. CREATE WEATHER DATAFRAME
# ============================================================

df_weather = pd.DataFrame(
    weather_results
)


# ============================================================
# 16. KEEP MAXIMUM 1500 ROWS
# ============================================================

df_weather = df_weather.head(
    TARGET_WEATHER
)


# ============================================================
# 17. ADD WEATHER RECORD ID
# ============================================================

df_weather.insert(
    0,
    "weather_id",
    range(
        1,
        len(df_weather) + 1
    )
)


# ============================================================
# 18. SAVE WEATHER DATA
# ============================================================

df_weather.to_csv(
    "weather_data.csv",
    index=False
)


# ============================================================
# 19. FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 60)
print("DATA COLLECTION COMPLETED")
print("=" * 60)


print(
    "Airport records:",
    len(df_airports)
)


print(
    "Flight records:",
    len(df_flights)
)


print(
    "Unique flight locations:",
    len(weather_locations)
)


print(
    "Weather records:",
    len(df_weather)
)


print("\nFiles created:")

print(
    "1. airport_data.csv"
)

print(
    "2. flight_data.csv"
)

print(
    "3. weather_data.csv"
)


print("\nWeather columns:")

print(
    list(df_weather.columns)
)


print("\nDone!")