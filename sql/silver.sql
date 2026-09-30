
DROP TABLE IF EXISTS silver.weather ;
DROP TABLE IF EXISTS silver.flights ;
DROP TABLE IF EXISTS silver.airports ;



-- =========================================================
-- SILVER FLIGHTS
-- =========================================================

CREATE TABLE silver.flights (
    flight_id TEXT PRIMARY KEY,
    icao24 TEXT,
    callsign TEXT,
    country TEXT,

    longitude NUMERIC,
    latitude NUMERIC,
    altitude_m NUMERIC,
    velocity_kmh NUMERIC,
    heading NUMERIC,
    vertical_rate NUMERIC,

    squawk TEXT,
    on_ground BOOLEAN,

    registration TEXT,
    model TEXT,
    typecode TEXT,

    source TEXT,
    source_quality TEXT,
    source_type TEXT,

    last_seen TIMESTAMP,
    last_contact TIMESTAMP,

    category TEXT,
    transport_kind TEXT,

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
    route_confidence TEXT,

    route_invalid BOOLEAN,
    speed_unreliable BOOLEAN,
    source_stale BOOLEAN
);


-- =========================================================
-- SILVER AIRPORTS
-- NO RELATION WITH FLIGHTS
-- =========================================================

CREATE TABLE silver.airports (
    iata TEXT PRIMARY KEY,
    icao TEXT,

    airport_name TEXT,
    city TEXT,
    state TEXT,
    country TEXT,

    elevation_m NUMERIC,
    timezone TEXT,
    airport_class TEXT,

    latitude NUMERIC,
    longitude NUMERIC
);


-- =========================================================
-- SILVER WEATHER
-- =========================================================

CREATE TABLE silver.weather (
    weather_id TEXT PRIMARY KEY,

    flight_id TEXT NOT NULL,

    flight_latitude NUMERIC,
    flight_longitude NUMERIC,

    weather_latitude NUMERIC,
    weather_longitude NUMERIC,

    weather_timezone TEXT,
    weather_elevation_m NUMERIC,

    temperature_celsius NUMERIC,
    relative_humidity_percentage NUMERIC,
    dew_point_celsius NUMERIC,
    apparent_temperature_celsius NUMERIC,

    precipitation_mm NUMERIC,
    rain_mm NUMERIC,
    showers_mm NUMERIC,
    snowfall_cm NUMERIC,
    snow_depth_m NUMERIC,

    weather_code INTEGER,
    cloud_cover_percentage NUMERIC,

    pressure_msl_hpa NUMERIC,
    surface_pressure_hpa NUMERIC,
    visibility_m NUMERIC,

    evapotranspiration_mm NUMERIC,
    vapour_pressure_deficit_kpa NUMERIC,

    wind_speed_kmh NUMERIC,
    wind_direction_degrees NUMERIC,
    wind_gusts_kmh NUMERIC,

    uv_index NUMERIC,
    uv_index_clear_sky NUMERIC,

    is_day BOOLEAN,

    sunshine_duration_seconds NUMERIC,
    cape_jkg NUMERIC,
    freezing_level_height_m NUMERIC,

    weather_time_utc TIMESTAMP,
    ingestion_timestamp_utc TIMESTAMP,

    CONSTRAINT fk_weather_flight
        FOREIGN KEY (flight_id)
        REFERENCES silver.flights(flight_id)
);


-- =========================================================
-- INSERT CLEAN FLIGHTS
-- =========================================================

WITH cleaned_flights AS
(
    SELECT
        NULLIF(TRIM(flight_id), '') AS flight_id,

        NULLIF(TRIM(icao24), '') AS icao24,
        NULLIF(TRIM(callsign), '') AS callsign,
        NULLIF(TRIM(country), '') AS country,

        CASE
            WHEN TRIM(lng) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(lng)::NUMERIC
            ELSE NULL
        END AS longitude,

        CASE
            WHEN TRIM(lat) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(lat)::NUMERIC
            ELSE NULL
        END AS latitude,

        CASE
            WHEN TRIM(alt) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(alt)::NUMERIC
            ELSE NULL
        END AS altitude_m,

        CASE
            WHEN TRIM(velocity) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(velocity)::NUMERIC
            ELSE NULL
        END AS velocity_kmh,

        CASE
            WHEN TRIM(heading) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(heading)::NUMERIC
            ELSE NULL
        END AS heading,

        CASE
            WHEN TRIM(vertical_rate) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(vertical_rate)::NUMERIC
            ELSE NULL
        END AS vertical_rate,

        NULLIF(TRIM(squawk), '') AS squawk,

        CASE
            WHEN LOWER(TRIM(on_ground)) IN ('true','1','yes')
            THEN TRUE
            WHEN LOWER(TRIM(on_ground)) IN ('false','0','no')
            THEN FALSE
            ELSE NULL
        END AS on_ground,

        NULLIF(TRIM(registration), '') AS registration,
        NULLIF(TRIM(model), '') AS model,
        NULLIF(TRIM(typecode), '') AS typecode,

        NULLIF(TRIM(source), '') AS source,
        NULLIF(TRIM(source_quality), '') AS source_quality,
        NULLIF(TRIM(source_type), '') AS source_type,

        CASE
            WHEN TRIM(last_seen) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TO_TIMESTAMP(TRIM(last_seen)::DOUBLE PRECISION)
            ELSE NULL
        END AS last_seen,

        CASE
            WHEN TRIM(last_contact) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TO_TIMESTAMP(TRIM(last_contact)::DOUBLE PRECISION)
            ELSE NULL
        END AS last_contact,

        NULLIF(TRIM(category), '') AS category,
        NULLIF(TRIM(transport_kind), '') AS transport_kind,

        NULLIF(TRIM(manufacturer), '') AS manufacturer,
        NULLIF(TRIM(operator), '') AS operator,
        NULLIF(TRIM(airline), '') AS airline,

        NULLIF(TRIM(origin), '') AS origin,
        NULLIF(TRIM(destination), '') AS destination,

        NULLIF(TRIM(origin_icao), '') AS origin_icao,
        NULLIF(TRIM(origin_iata), '') AS origin_iata,

        NULLIF(TRIM(destination_icao), '') AS destination_icao,
        NULLIF(TRIM(destination_iata), '') AS destination_iata,

        NULLIF(TRIM(route_source), '') AS route_source,

        CASE
            WHEN LOWER(TRIM(route_confidence))
                 IN ('unknown','null','none','')
            THEN NULL
            ELSE TRIM(route_confidence)
        END AS route_confidence,

        CASE
            WHEN LOWER(TRIM(route_invalid)) IN ('true','1','yes')
            THEN TRUE
            WHEN LOWER(TRIM(route_invalid)) IN ('false','0','no')
            THEN FALSE
            ELSE NULL
        END AS route_invalid,

        CASE
            WHEN LOWER(TRIM(speed_unreliable)) IN ('true','1','yes')
            THEN TRUE
            WHEN LOWER(TRIM(speed_unreliable)) IN ('false','0','no')
            THEN FALSE
            ELSE NULL
        END AS speed_unreliable,

        CASE
            WHEN LOWER(TRIM(source_stale)) IN ('true','1','yes')
            THEN TRUE
            WHEN LOWER(TRIM(source_stale)) IN ('false','0','no')
            THEN FALSE
            ELSE NULL
        END AS source_stale,

        ROW_NUMBER() OVER (
            PARTITION BY flight_id
            ORDER BY last_contact DESC NULLS LAST
        ) AS rn

    FROM bronze.flightdata
)

INSERT INTO silver.flights
SELECT
    flight_id,
    icao24,
    callsign,
    country,
    longitude,
    latitude,
    altitude_m,
    velocity_kmh,
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
    route_confidence,
    route_invalid,
    speed_unreliable,
    source_stale
FROM cleaned_flights
WHERE rn = 1
  AND flight_id IS NOT NULL;


-- =========================================================
-- INSERT CLEAN AIRPORTS
-- =========================================================

WITH cleaned_airports AS
(
    SELECT
        NULLIF(TRIM(iata), '') AS iata,
        NULLIF(TRIM(icao), '') AS icao,

        NULLIF(TRIM(name), '') AS airport_name,
        NULLIF(TRIM(city), '') AS city,
        NULLIF(TRIM(state), '') AS state,
        NULLIF(TRIM(country), '') AS country,

        CASE
            WHEN TRIM(elevation) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(elevation)::NUMERIC
            ELSE NULL
        END AS elevation_m,

        NULLIF(TRIM(tz), '') AS timezone,
        NULLIF(TRIM(airport_class), '') AS airport_class,

        CASE
            WHEN TRIM(lat) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(lat)::NUMERIC
            ELSE NULL
        END AS latitude,

        CASE
            WHEN TRIM(lng) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(lng)::NUMERIC
            ELSE NULL
        END AS longitude,

        ROW_NUMBER() OVER (
            PARTITION BY iata
            ORDER BY iata
        ) AS rn

    FROM bronze.airportdata
)

INSERT INTO silver.airports
SELECT
    iata,
    icao,
    airport_name,
    city,
    state,
    country,
    elevation_m,
    timezone,
    airport_class,
    latitude,
    longitude
FROM cleaned_airports
WHERE rn = 1
  AND iata IS NOT NULL;


-- =========================================================
-- INSERT CLEAN WEATHER
-- ONLY WEATHER WITH A VALID SILVER FLIGHT
-- =========================================================

WITH cleaned_weather AS
(
    SELECT
        NULLIF(TRIM(w.weather_id), '') AS weather_id,

        NULLIF(TRIM(w.flight_id), '') AS flight_id,

        CASE
            WHEN TRIM(w.flight_latitude) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.flight_latitude)::NUMERIC
            ELSE NULL
        END AS flight_latitude,

        CASE
            WHEN TRIM(w.flight_longitude) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.flight_longitude)::NUMERIC
            ELSE NULL
        END AS flight_longitude,

        CASE
            WHEN TRIM(w.weather_latitude) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.weather_latitude)::NUMERIC
            ELSE NULL
        END AS weather_latitude,

        CASE
            WHEN TRIM(w.weather_longitude) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.weather_longitude)::NUMERIC
            ELSE NULL
        END AS weather_longitude,

        NULLIF(TRIM(w.weather_timezone), '') AS weather_timezone,

        CASE
            WHEN TRIM(w.weather_elevation_m) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.weather_elevation_m)::NUMERIC
            ELSE NULL
        END AS weather_elevation_m,

        CASE
            WHEN TRIM(w.temperature_celsius) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.temperature_celsius)::NUMERIC
            ELSE NULL
        END AS temperature_celsius,

        CASE
            WHEN TRIM(w.relative_humidity_percentage) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.relative_humidity_percentage)::NUMERIC
            ELSE NULL
        END AS relative_humidity_percentage,

        CASE
            WHEN TRIM(w.dew_point_celsius) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.dew_point_celsius)::NUMERIC
            ELSE NULL
        END AS dew_point_celsius,

        CASE
            WHEN TRIM(w.apparent_temperature_celsius) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.apparent_temperature_celsius)::NUMERIC
            ELSE NULL
        END AS apparent_temperature_celsius,

        CASE
            WHEN TRIM(w.precipitation_mm) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.precipitation_mm)::NUMERIC
            ELSE NULL
        END AS precipitation_mm,

        CASE
            WHEN TRIM(w.rain_mm) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.rain_mm)::NUMERIC
            ELSE NULL
        END AS rain_mm,

        CASE
            WHEN TRIM(w.showers_mm) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.showers_mm)::NUMERIC
            ELSE NULL
        END AS showers_mm,

        CASE
            WHEN TRIM(w.snowfall_cm) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.snowfall_cm)::NUMERIC
            ELSE NULL
        END AS snowfall_cm,

        CASE
            WHEN TRIM(w.snow_depth_m) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.snow_depth_m)::NUMERIC
            ELSE NULL
        END AS snow_depth_m,

        CASE
            WHEN TRIM(w.weather_code) ~ '^-?[0-9]+$'
            THEN TRIM(w.weather_code)::INTEGER
            ELSE NULL
        END AS weather_code,

        CASE
            WHEN TRIM(w.cloud_cover_percentage) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.cloud_cover_percentage)::NUMERIC
            ELSE NULL
        END AS cloud_cover_percentage,

        CASE
            WHEN TRIM(w.pressure_msl_hpa) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.pressure_msl_hpa)::NUMERIC
            ELSE NULL
        END AS pressure_msl_hpa,

        CASE
            WHEN TRIM(w.surface_pressure_hpa) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.surface_pressure_hpa)::NUMERIC
            ELSE NULL
        END AS surface_pressure_hpa,

        CASE
            WHEN TRIM(w.visibility_m) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.visibility_m)::NUMERIC
            ELSE NULL
        END AS visibility_m,

        CASE
            WHEN TRIM(w.evapotranspiration_mm) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.evapotranspiration_mm)::NUMERIC
            ELSE NULL
        END AS evapotranspiration_mm,

        CASE
            WHEN TRIM(w.vapour_pressure_deficit_kpa) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.vapour_pressure_deficit_kpa)::NUMERIC
            ELSE NULL
        END AS vapour_pressure_deficit_kpa,

        CASE
            WHEN TRIM(w.wind_speed_kmh) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.wind_speed_kmh)::NUMERIC
            ELSE NULL
        END AS wind_speed_kmh,

        CASE
            WHEN TRIM(w.wind_direction_degrees) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.wind_direction_degrees)::NUMERIC
            ELSE NULL
        END AS wind_direction_degrees,

        CASE
            WHEN TRIM(w.wind_gusts_kmh) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.wind_gusts_kmh)::NUMERIC
            ELSE NULL
        END AS wind_gusts_kmh,

        CASE
            WHEN TRIM(w.uv_index) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.uv_index)::NUMERIC
            ELSE NULL
        END AS uv_index,

        CASE
            WHEN TRIM(w.uv_index_clear_sky) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.uv_index_clear_sky)::NUMERIC
            ELSE NULL
        END AS uv_index_clear_sky,

        CASE
            WHEN LOWER(TRIM(w.is_day)) IN ('true','1','yes')
            THEN TRUE
            WHEN LOWER(TRIM(w.is_day)) IN ('false','0','no')
            THEN FALSE
            ELSE NULL
        END AS is_day,

        CASE
            WHEN TRIM(w.sunshine_duration_seconds) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.sunshine_duration_seconds)::NUMERIC
            ELSE NULL
        END AS sunshine_duration_seconds,

        CASE
            WHEN TRIM(w.cape_jkg) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.cape_jkg)::NUMERIC
            ELSE NULL
        END AS cape_jkg,

        CASE
            WHEN TRIM(w.freezing_level_height_m) ~ '^-?[0-9]+(\.[0-9]+)?$'
            THEN TRIM(w.freezing_level_height_m)::NUMERIC
            ELSE NULL
        END AS freezing_level_height_m,

        CASE
            WHEN TRIM(w.weather_time_utc) <> ''
            THEN TRIM(w.weather_time_utc)::TIMESTAMP
            ELSE NULL
        END AS weather_time_utc,

        CASE
            WHEN TRIM(w.ingestion_timestamp_utc) <> ''
            THEN TRIM(w.ingestion_timestamp_utc)::TIMESTAMP
            ELSE NULL
        END AS ingestion_timestamp_utc,

        ROW_NUMBER() OVER (
            PARTITION BY w.weather_id
            ORDER BY w.ingestion_timestamp_utc DESC NULLS LAST
        ) AS rn

    FROM bronze.weatherdata w
)

INSERT INTO silver.weather
SELECT
    w.weather_id,
    w.flight_id,
    w.flight_latitude,
    w.flight_longitude,
    w.weather_latitude,
    w.weather_longitude,
    w.weather_timezone,
    w.weather_elevation_m,
    w.temperature_celsius,
    w.relative_humidity_percentage,
    w.dew_point_celsius,
    w.apparent_temperature_celsius,
    w.precipitation_mm,
    w.rain_mm,
    w.showers_mm,
    w.snowfall_cm,
    w.snow_depth_m,
    w.weather_code,
    w.cloud_cover_percentage,
    w.pressure_msl_hpa,
    w.surface_pressure_hpa,
    w.visibility_m,
    w.evapotranspiration_mm,
    w.vapour_pressure_deficit_kpa,
    w.wind_speed_kmh,
    w.wind_direction_degrees,
    w.wind_gusts_kmh,
    w.uv_index,
    w.uv_index_clear_sky,
    w.is_day,
    w.sunshine_duration_seconds,
    w.cape_jkg,
    w.freezing_level_height_m,
    w.weather_time_utc,
    w.ingestion_timestamp_utc
FROM cleaned_weather w
INNER JOIN silver.flights f
    ON f.flight_id = w.flight_id
WHERE w.rn = 1
  AND w.weather_id IS NOT NULL
  AND w.flight_id IS NOT NULL;


-- =========================================================
-- CHECK RESULTS
-- =========================================================

SELECT 'Flights' AS table_name,
       COUNT(*) AS total_rows
FROM silver.flights

UNION ALL

SELECT 'Airports',
       COUNT(*)
FROM silver.airports

UNION ALL

SELECT 'Weather',
       COUNT(*)
FROM silver.weather;


-- =========================================================
-- VIEW SILVER DATA
-- =========================================================

SELECT *
FROM silver.flights;

SELECT *
FROM silver.airports;

SELECT *
FROM silver.weather;

