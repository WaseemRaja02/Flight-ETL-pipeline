from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd


def get_connection():
    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password="waseemraja",
        host="localhost",
        port=5432,
        database="final"
    )

    return create_engine(connection_url)


def get_gold_data():

    engine = get_connection()

    dashboard_kpis = pd.read_sql(
        "SELECT * FROM gold.dashboard_kpis;",
        engine
    )

    flight_weather = pd.read_sql(
        "SELECT * FROM gold.flight_weather;",
        engine
    )

    airline_summary = pd.read_sql(
        "SELECT * FROM gold.airline_summary;",
        engine
    )

    country_summary = pd.read_sql(
        "SELECT * FROM gold.country_summary;",
        engine
    )

    airport_summary = pd.read_sql(
        "SELECT * FROM gold.airport_summary;",
        engine
    )

    weather_summary = pd.read_sql(
        "SELECT * FROM gold.weather_summary;",
        engine
    )

    engine.dispose()

    return (
        dashboard_kpis,
        flight_weather,
        airline_summary,
        country_summary,
        airport_summary,
        weather_summary
    )