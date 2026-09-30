DROP VIEW IF EXISTS gold.dashboard_kpis CASCADE;
DROP VIEW IF EXISTS gold.flight_weather CASCADE;
DROP VIEW IF EXISTS gold.airline_summary CASCADE;
DROP VIEW IF EXISTS gold.country_summary CASCADE;
DROP VIEW IF EXISTS gold.airport_summary CASCADE;
DROP VIEW IF EXISTS gold.weather_summary CASCADE;


-- =========================================================
-- 1. DASHBOARD KPIs
-- =========================================================

CREATE VIEW gold.dashboard_kpis AS
SELECT
    COUNT(DISTINCT f.flight_id) AS total_flights,

    COUNT(DISTINCT f.flight_id)
        FILTER (WHERE f.on_ground = TRUE) AS flights_on_ground,

    COUNT(DISTINCT f.flight_id)
        FILTER (WHERE f.on_ground = FALSE) AS flights_in_air,

    COUNT(DISTINCT f.country) AS total_countries,

    COUNT(DISTINCT f.origin_iata) AS total_origins,

    COUNT(DISTINCT f.destination_iata) AS total_destinations,

    COUNT(DISTINCT w.weather_id) AS total_weather_records,

    ROUND(AVG(f.altitude_m), 2) AS average_altitude_m,

    ROUND(AVG(f.velocity_kmh), 2) AS average_velocity_kmh,

    ROUND(AVG(w.temperature_celsius), 2) AS average_temperature_celsius,

    ROUND(AVG(w.relative_humidity_percentage), 2)
        AS average_humidity_percentage,

    ROUND(AVG(w.wind_speed_kmh), 2)
        AS average_wind_speed_kmh

FROM silver.flights f
LEFT JOIN silver.weather w
    ON f.flight_id = w.flight_id;


-- =========================================================
-- 2. MAIN FLIGHT + WEATHER RELATION
-- =========================================================

DROP VIEW gold.flight_weather;

CREATE OR REPLACE VIEW gold.flight_weather AS
SELECT
    f.flight_id,

    f.icao24,
    f.callsign,
    f.country,

    f.latitude AS flight_latitude,
    f.longitude AS flight_longitude,

    f.altitude_m,
    f.velocity_kmh,
    f.heading,
    f.vertical_rate,

    f.on_ground,
    f.category,
    f.transport_kind,

    w.weather_id,

    w.weather_latitude,
    w.weather_longitude,

    w.temperature_celsius,
    w.relative_humidity_percentage,

    w.apparent_temperature_celsius,

    w.precipitation_mm,
    w.rain_mm,

    w.weather_code,
    w.cloud_cover_percentage,

    w.pressure_msl_hpa,
    w.visibility_m,

    w.wind_speed_kmh,
    w.wind_direction_degrees,
    w.wind_gusts_kmh,

    w.uv_index,
    w.is_day,

    w.weather_time_utc

FROM silver.flights f

INNER JOIN silver.weather w
    ON f.flight_id = w.flight_id;


-- =========================================================
-- 3. AIRLINE SUMMARY
-- Only use airline if it has actual values
-- =========================================================

CREATE or REPLACE VIEW gold.airline_summary AS
SELECT
    f.airline,

    COUNT(*) AS total_flights,

    COUNT(*) FILTER (
        WHERE f.on_ground = TRUE
    ) AS flights_on_ground,

    COUNT(*) FILTER (
        WHERE f.on_ground = FALSE
    ) AS flights_in_air,

    ROUND(AVG(f.altitude_m), 2)
        AS average_altitude_m,

    ROUND(AVG(f.velocity_kmh), 2)
        AS average_velocity_kmh

FROM silver.flights f

WHERE f.airline IS NOT NULL
  AND TRIM(f.airline) <> ''

GROUP BY f.airline;


-- =========================================================
-- 4. COUNTRY SUMMARY
-- =========================================================

CREATE VIEW gold.country_summary AS
SELECT
    f.country,

    COUNT(*) AS total_flights,

    COUNT(DISTINCT f.airline)
        FILTER (
            WHERE f.airline IS NOT NULL
            AND TRIM(f.airline) <> ''
        ) AS airlines,

    COUNT(*) FILTER (
        WHERE f.on_ground = TRUE
    ) AS flights_on_ground,

    COUNT(*) FILTER (
        WHERE f.on_ground = FALSE
    ) AS flights_in_air,

    ROUND(AVG(f.altitude_m), 2)
        AS average_altitude_m,

    ROUND(AVG(f.velocity_kmh), 2)
        AS average_velocity_kmh

FROM silver.flights f

WHERE f.country IS NOT NULL
  AND TRIM(f.country) <> ''

GROUP BY f.country;


-- =========================================================
-- 5. AIRPORT SUMMARY
-- Airports stay independent
-- =========================================================

CREATE VIEW gold.airport_summary AS
SELECT
    a.country,

    COUNT(*) AS total_airports,

    COUNT(DISTINCT a.city) AS total_cities,

    ROUND(AVG(a.elevation_m), 2)
        AS average_elevation_m,

    ROUND(MAX(a.elevation_m), 2)
        AS highest_airport_elevation_m,

    ROUND(MIN(a.elevation_m), 2)
        AS lowest_airport_elevation_m

FROM silver.airports a

WHERE a.country IS NOT NULL
  AND TRIM(a.country) <> ''

GROUP BY a.country;


-- =========================================================
-- 6. WEATHER SUMMARY
-- =========================================================

CREATE VIEW gold.weather_summary AS
SELECT

    COUNT(*) AS total_weather_records,

    COUNT(DISTINCT flight_id)
        AS flights_with_weather,

    ROUND(AVG(temperature_celsius), 2)
        AS average_temperature_celsius,

    ROUND(MIN(temperature_celsius), 2)
        AS minimum_temperature_celsius,

    ROUND(MAX(temperature_celsius), 2)
        AS maximum_temperature_celsius,

    ROUND(AVG(relative_humidity_percentage), 2)
        AS average_humidity_percentage,

    ROUND(AVG(wind_speed_kmh), 2)
        AS average_wind_speed_kmh,

    ROUND(MAX(wind_speed_kmh), 2)
        AS maximum_wind_speed_kmh,

    ROUND(AVG(visibility_m), 2)
        AS average_visibility_m,

    ROUND(AVG(cloud_cover_percentage), 2)
        AS average_cloud_cover_percentage,

    ROUND(AVG(pressure_msl_hpa), 2)
        AS average_pressure_msl_hpa,

    ROUND(AVG(uv_index), 2)
        AS average_uv_index,

    ROUND(SUM(precipitation_mm), 2)
        AS total_precipitation_mm

FROM silver.weather;


-- =========================================================
-- CHECK GOLD TABLES
-- =========================================================

SELECT * FROM gold.dashboard_kpis;

SELECT * FROM gold.flight_weather;

SELECT * FROM gold.airline_summary;

SELECT * FROM gold.country_summary;

SELECT * FROM gold.airport_summary;

SELECT * FROM gold.weather_summary;

SELECT *
FROM gold.flight_weather
LIMIT 1;





