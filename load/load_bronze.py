import psycopg2
import pandas as pd


DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "final"
DB_USER = "postgres"
DB_PASSWORD = "waseemraja"


FLIGHT_CSV = r"C:\Users\LENOVO\OneDrive\Desktop\weather_data pakistan\extractor\flight_data.csv"
AIRPORT_CSV = r"C:\Users\LENOVO\OneDrive\Desktop\weather_data pakistan\extractor\airport_data.csv"
WEATHER_CSV = r"C:\Users\LENOVO\OneDrive\Desktop\weather_data pakistan\extractor\weather_data.csv"


conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()


# ============================================================
# FLIGHT DATA
# ============================================================

print("Loading flight data...")

df_flight = pd.read_csv(
    FLIGHT_CSV,
    dtype=str,
    keep_default_na=False,
    low_memory=False
)

flight_columns = [
    "icao24",
    "callsign",
    "country",
    "lng",
    "lat",
    "alt",
    "velocity",
    "heading",
    "vertical_rate",
    "squawk",
    "on_ground",
    "registration",
    "model",
    "typecode",
    "source",
    "source_quality",
    "source_type",
    "last_seen",
    "last_contact",
    "category",
    "transport_kind",
    "icon_key",
    "icon_emoji",
    "icon_color",
    "route_confidence",
    "display_heading",
    "cache_stale",
    "manufacturer",
    "operator",
    "airline",
    "origin",
    "destination",
    "origin_icao",
    "origin_iata",
    "destination_icao",
    "destination_iata",
    "route_source",
    "route_invalid",
    "route_rejected_reason",
    "speed_unreliable",
    "source_stale",
    "flight_id"
]

df_flight = df_flight[
    flight_columns
]


flight_sql = """
INSERT INTO bronze.flightdata (
    icao24,
    callsign,
    country,
    lng,
    lat,
    alt,
    velocity,
    heading,
    vertical_rate,
    squawk,
    on_ground,
    registration,
    model,
    typecode,
    source,
    source_quality,
    source_type,
    last_seen,
    last_contact,
    category,
    transport_kind,
    icon_key,
    icon_emoji,
    icon_color,
    route_confidence,
    display_heading,
    cache_stale,
    manufacturer,
    operator,
    airline,
    origin,
    destination,
    origin_icao,
    origin_iata,
    destination_icao,
    destination_iata,
    route_source,
    route_invalid,
    route_rejected_reason,
    speed_unreliable,
    source_stale,
    flight_id
)
VALUES (
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s
)
"""


for _, row in df_flight.iterrows():

    cursor.execute(
        flight_sql,
        tuple(row)
    )


print(
    "Flight rows inserted:",
    len(df_flight)
)


# ============================================================
# AIRPORT DATA
# ============================================================

print("Loading airport data...")

df_airport = pd.read_csv(
    AIRPORT_CSV,
    dtype=str,
    keep_default_na=False,
    low_memory=False
)

airport_columns = [
    "iata",
    "icao",
    "name",
    "city",
    "state",
    "country",
    "elevation",
    "tz",
    "airport_class",
    "lat",
    "lng"
]

df_airport = df_airport[
    airport_columns
]


airport_sql = """
INSERT INTO bronze.airportdata (
    iata,
    icao,
    name,
    city,
    state,
    country,
    elevation,
    tz,
    airport_class,
    lat,
    lng
)
VALUES (
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)
"""


for _, row in df_airport.iterrows():

    cursor.execute(
        airport_sql,
        tuple(row)
    )


print(
    "Airport rows inserted:",
    len(df_airport)
)


# ============================================================
# WEATHER DATA
# ============================================================

print("Loading weather data...")

df_weather = pd.read_csv(
    WEATHER_CSV,
    dtype=str,
    keep_default_na=False,
    low_memory=False
)

weather_columns = [
    "weather_id",
    "flight_id",
    "flight_latitude",
    "flight_longitude",
    "weather_latitude",
    "weather_longitude",
    "weather_timezone",
    "weather_elevation_m",
    "temperature_celsius",
    "relative_humidity_percentage",
    "dew_point_celsius",
    "apparent_temperature_celsius",
    "precipitation_mm",
    "rain_mm",
    "showers_mm",
    "snowfall_cm",
    "snow_depth_m",
    "weather_code",
    "cloud_cover_percentage",
    "pressure_msl_hpa",
    "surface_pressure_hpa",
    "visibility_m",
    "evapotranspiration_mm",
    "vapour_pressure_deficit_kpa",
    "wind_speed_kmh",
    "wind_direction_degrees",
    "wind_gusts_kmh",
    "uv_index",
    "uv_index_clear_sky",
    "is_day",
    "sunshine_duration_seconds",
    "cape_jkg",
    "freezing_level_height_m",
    "weather_time_utc",
    "ingestion_timestamp_utc"
]

df_weather = df_weather[
    weather_columns
]


weather_sql = """
INSERT INTO bronze.weatherdata (
    weather_id,
    flight_id,
    flight_latitude,
    flight_longitude,
    weather_latitude,
    weather_longitude,
    weather_timezone,
    weather_elevation_m,
    temperature_celsius,
    relative_humidity_percentage,
    dew_point_celsius,
    apparent_temperature_celsius,
    precipitation_mm,
    rain_mm,
    showers_mm,
    snowfall_cm,
    snow_depth_m,
    weather_code,
    cloud_cover_percentage,
    pressure_msl_hpa,
    surface_pressure_hpa,
    visibility_m,
    evapotranspiration_mm,
    vapour_pressure_deficit_kpa,
    wind_speed_kmh,
    wind_direction_degrees,
    wind_gusts_kmh,
    uv_index,
    uv_index_clear_sky,
    is_day,
    sunshine_duration_seconds,
    cape_jkg,
    freezing_level_height_m,
    weather_time_utc,
    ingestion_timestamp_utc
)
VALUES (
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s
)
"""


for _, row in df_weather.iterrows():

    cursor.execute(
        weather_sql,
        tuple(row)
    )


print(
    "Weather rows inserted:",
    len(df_weather)
)


# ============================================================
# COMMIT
# ============================================================

conn.commit()

cursor.close()
conn.close()


print()
print("=" * 60)
print("BRONZE DATA IMPORT COMPLETED")
print("=" * 60)
print(
    "Flight rows:",
    len(df_flight)
)
print(
    "Airport rows:",
    len(df_airport)
)
print(
    "Weather rows:",
    len(df_weather)
)
print("=" * 60)