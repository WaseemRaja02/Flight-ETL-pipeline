CREATE SCHEMA bronze;

DROP TABLE IF EXISTS bronze.flightdata;

CREATE TABLE bronze.flightdata (
    icao24 TEXT,
    callsign TEXT,
    country TEXT,
    lng TEXT,
    lat TEXT,
    alt TEXT,
    velocity TEXT,
    heading TEXT,
    vertical_rate TEXT,
    squawk TEXT,
    on_ground TEXT,
    registration TEXT,
    model TEXT,
    typecode TEXT,
    source TEXT,
    source_quality TEXT,
    source_type TEXT,
    last_seen TEXT,
    last_contact TEXT,
    category TEXT,
    transport_kind TEXT,
    icon_key TEXT,
    icon_emoji TEXT,
    icon_color TEXT,
    route_confidence TEXT,
    display_heading TEXT,
    cache_stale TEXT,
    manufacturer TEXT,
    operator TEXT,
    airline TEXT,
    origin TEXT,
    destination TEXT,
    origin_icao TEXT,
    origin_iata TEXT,
    destination_icao TEXT,
    destination_iata TEXT,
    route_source TEXT,
    route_invalid TEXT,
    route_rejected_reason TEXT,
    speed_unreliable TEXT,
    source_stale TEXT,
    flight_id TEXT
);


  DROP TABLE IF EXISTS bronze.airportdata;

CREATE TABLE bronze.airportdata (
    iata TEXT,
    icao TEXT,
    name TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    elevation TEXT,
    tz TEXT,
    airport_class TEXT,
    lat TEXT,
    lng TEXT
);

DROP TABLE IF EXISTS bronze.weatherdata;

CREATE TABLE bronze.weatherdata (
    weather_id TEXT,
    flight_id TEXT,
    flight_latitude TEXT,
    flight_longitude TEXT,
    weather_latitude TEXT,
    weather_longitude TEXT,
    weather_timezone TEXT,
    weather_elevation_m TEXT,
    temperature_celsius TEXT,
    relative_humidity_percentage TEXT,
    dew_point_celsius TEXT,
    apparent_temperature_celsius TEXT,
    precipitation_mm TEXT,
    rain_mm TEXT,
    showers_mm TEXT,
    snowfall_cm TEXT,
    snow_depth_m TEXT,
    weather_code TEXT,
    cloud_cover_percentage TEXT,
    pressure_msl_hpa TEXT,
    surface_pressure_hpa TEXT,
    visibility_m TEXT,
    evapotranspiration_mm TEXT,
    vapour_pressure_deficit_kpa TEXT,
    wind_speed_kmh TEXT,
    wind_direction_degrees TEXT,
    wind_gusts_kmh TEXT,
    uv_index TEXT,
    uv_index_clear_sky TEXT,
    is_day TEXT,
    sunshine_duration_seconds TEXT,
    cape_jkg TEXT,
    freezing_level_height_m TEXT,
    weather_time_utc TEXT,
    ingestion_timestamp_utc TEXT
);

select * from bronze.flightdata
select * from bronze.airportdata
select * from bronze.weatherdata

