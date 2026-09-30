import streamlit as st
import pandas as pd
import plotly.express as px
import base64

from database import get_gold_data


st.set_page_config(
    page_title="Flight & Weather Analytics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("world.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()


st.markdown(
    f"""
    <style>

    html, body {{
        background: transparent !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background: transparent !important;
    }}

    [data-testid="stMain"] {{
        background: transparent !important;
    }}

    .stApp {{
        min-height: 100vh;
        background-image:
            linear-gradient(
                rgba(11, 17, 32, 0.82),
                rgba(11, 17, 32, 0.82)
            ),
            url("data:image/jpeg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }}

    [data-testid="stToolbar"] {{
        background: transparent !important;
        background-color: transparent !important;
    }}

    [data-testid="stDecoration"] {{
        background: transparent !important;
    }}

    [data-testid="stStatusWidget"] {{
        background: transparent !important;
    }}

    [data-testid="stHeader"] button {{
        background-color: rgba(15, 23, 42, 0.65) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(71, 85, 105, 0.75) !important;
        border-radius: 8px !important;
    }}

    [data-testid="stHeader"] button:hover {{
        background-color: rgba(51, 65, 85, 0.90) !important;
    }}

    [data-testid="stMainBlockContainer"] {{
        padding-top: 3.5rem;
        padding-bottom: 2rem;
    }}

    section[data-testid="stSidebar"] {{
        background-color: rgba(15, 23, 42, 0.97) !important;
        border-right: 1px solid #334155;
    }}

    section[data-testid="stSidebar"] > div {{
        background-color: transparent !important;
    }}

    .sidebar-title {{
        font-size: 21px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 3px;
    }}

    .sidebar-subtitle {{
        color: #94a3b8;
        font-size: 12px;
        margin-bottom: 25px;
    }}

    .main-title {{
        font-size: 32px;
        font-weight: 800;
        line-height: 1.3;
        color: #f8fafc;
        margin-top: 0;
        margin-bottom: 6px;
    }}

    .main-subtitle {{
        font-size: 14px;
        line-height: 1.5;
        color: #cbd5e1;
        margin-bottom: 25px;
    }}

    .section-header {{
        font-size: 20px;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 18px;
        margin-bottom: 12px;
        padding-left: 10px;
        border-left: 4px solid #38bdf8;
    }}

    div[data-testid="stMetric"] {{
        background-color: rgba(30, 41, 59, 0.94) !important;
        border: 1px solid #475569 !important;
        border-radius: 12px;
        padding: 16px;
        min-height: 100px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.20);
    }}

    div[data-testid="stMetric"]:hover {{
        background-color: rgba(36, 50, 72, 0.97) !important;
        border-color: #38bdf8 !important;
    }}

    div[data-testid="stMetricLabel"] {{
        color: #cbd5e1 !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: #f8fafc !important;
        font-weight: 700 !important;
    }}

    div[data-testid="stMetricDelta"] {{
        color: #94a3b8 !important;
    }}

    .info-bar {{
        background-color: rgba(30, 41, 59, 0.94) !important;
        border: 1px solid #475569;
        border-radius: 10px;
        padding: 10px 15px;
        margin: 10px 0 20px 0;
        color: #e2e8f0;
        font-size: 13px;
    }}

    section[data-testid="stSidebar"] label {{
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }}

    section[data-testid="stSidebar"] p {{
        color: #cbd5e1 !important;
    }}

    section[data-testid="stSidebar"] span {{
        color: #cbd5e1;
    }}

    div[data-baseweb="select"] > div {{
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
        min-height: 42px;
    }}

    div[data-baseweb="select"] > div:hover {{
        border-color: #64748b !important;
    }}

    div[data-baseweb="select"] span {{
        color: #f1f5f9 !important;
    }}

    div[data-baseweb="select"] svg {{
        fill: #cbd5e1 !important;
    }}

    div[role="listbox"] {{
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
    }}

    div[role="option"] {{
        background-color: #1e293b !important;
        color: #f8fafc !important;
    }}

    div[role="option"]:hover {{
        background-color: #334155 !important;
        color: #ffffff !important;
    }}

    div[role="option"][aria-selected="true"] {{
        background-color: #334155 !important;
        color: #38bdf8 !important;
    }}

    span[data-baseweb="tag"] {{
        background-color: #334155 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 6px !important;
    }}

    span[data-baseweb="tag"] span {{
        color: #f8fafc !important;
    }}

    span[data-baseweb="tag"] svg {{
        fill: #cbd5e1 !important;
    }}

    div[data-baseweb="input"] {{
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }}

    div[data-baseweb="input"]:focus-within {{
        border-color: #38bdf8 !important;
    }}

    div[data-baseweb="input"] input {{
        color: #f8fafc !important;
        background-color: transparent !important;
    }}

    div[data-testid="stSlider"] {{
        color: #38bdf8 !important;
    }}

    div[data-testid="stSlider"] label {{
        color: #cbd5e1 !important;
    }}

    div[data-testid="stCheckbox"] label {{
        color: #cbd5e1 !important;
    }}

    div[data-testid="stRadio"] label {{
        color: #cbd5e1 !important;
    }}

    div[data-testid="stPlotlyChart"] {{
        background-color: rgba(30, 41, 59, 0.94) !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
        padding: 8px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.20);
    }}

    div[data-testid="stPlotlyChart"]:hover {{
        border-color: #64748b !important;
    }}

    div[data-testid="stDataFrame"] {{
        background-color: rgba(30, 41, 59, 0.94) !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
    }}

    .stButton > button {{
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }}

    .stButton > button:hover {{
        background-color: #334155 !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
    }}

    div[data-testid="stExpander"] {{
        background-color: rgba(30, 41, 59, 0.94) !important;
        border: 1px solid #475569 !important;
        border-radius: 10px !important;
    }}

    div[data-testid="stExpander"] summary {{
        color: #f8fafc !important;
    }}

    .stMarkdown {{
        color: #e2e8f0;
    }}

    p {{
        color: #cbd5e1;
    }}

    .footer {{
        text-align: center;
        color: #64748b;
        font-size: 11px;
        margin-top: 35px;
        padding-top: 15px;
        border-top: 1px solid #334155;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


def safe_unique(data, column):

    if column not in data.columns:
        return []

    values = (
        data[column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    values = values[values != ""]

    return sorted(values.unique().tolist())


def numeric_column(data, column):

    if column not in data.columns:
        return pd.Series(
            index=data.index,
            dtype="float64"
        )

    return pd.to_numeric(
        data[column],
        errors="coerce"
    )


def average(data, column):

    values = numeric_column(
        data,
        column
    ).dropna()

    if values.empty:
        return None

    return values.mean()


def number_format(value):

    if value is None:
        return "0"

    try:
        if pd.isna(value):
            return "0"

        return f"{value:,.0f}"

    except:
        return "0"


def decimal_format(value, digits=1):

    if value is None:
        return "—"

    try:

        if pd.isna(value):
            return "—"

        return f"{value:,.{digits}f}"

    except:

        return "—"


def chart_style(fig, height=390):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#e5e7eb"),
        height=height,
        margin=dict(
            l=40,
            r=30,
            t=60,
            b=40
        )
    )

    fig.update_xaxes(
        gridcolor="#1e293b",
        zerolinecolor="#1e293b"
    )

    fig.update_yaxes(
        gridcolor="#1e293b",
        zerolinecolor="#1e293b"
    )

    return fig


@st.cache_data(ttl=300)
def load_data():

    return get_gold_data()


try:

    (
        dashboard_kpis,
        flight_weather,
        airline_summary,
        country_summary,
        airport_summary,
        weather_summary
    ) = load_data()

    dashboard_kpis.columns = [
        str(column).strip().lower()
        for column in dashboard_kpis.columns
    ]

except Exception as e:

    st.error(
        "Could not load data from PostgreSQL Gold layer."
    )

    st.exception(e)

    st.stop()


df = flight_weather.copy()

df.columns = [
    str(column).strip().lower()
    for column in df.columns
]


airport_df = airport_summary.copy()

airport_df.columns = [
    str(column).strip().lower()
    for column in airport_df.columns
]


if df.empty:

    st.warning(
        "No records found in gold.flight_weather."
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">✈️ Flight & Weather Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-subtitle">
        Enterprise flight operations, weather intelligence and airport analytics
        powered by PostgreSQL Gold layer.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">Filters</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Flight & Weather Controls</div>',
        unsafe_allow_html=True
    )

    country_options = safe_unique(
        df,
        "country"
    )

    selected_country = st.multiselect(
        "🌍 Country",
        country_options
    )

    selected_status = st.multiselect(
        "✈️ Flight Status",
        ["In Air", "On Ground"]
    )

    transport_options = safe_unique(
        df,
        "transport_kind"
    )

    selected_transport = st.multiselect(
        "🚍 Transport Type",
        transport_options
    )

    category_options = safe_unique(
        df,
        "category"
    )

    selected_category = st.multiselect(
        "🛩️ Aircraft Category",
        category_options
    )

    selected_time = st.multiselect(
        "🌞 Time of Day",
        ["Day", "Night"]
    )

    if "weather_time_utc" in df.columns:

        weather_dates = pd.to_datetime(
            df["weather_time_utc"],
            errors="coerce"
        ).dt.date.dropna().unique()

        weather_dates = sorted(
            weather_dates
        )

    else:

        weather_dates = []

    selected_date = st.multiselect(
        "📅 Weather Date",
        weather_dates
    )


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


if selected_country:

    filtered_df = filtered_df[
        filtered_df["country"]
        .astype(str)
        .isin(selected_country)
    ]


if selected_status:

    status_mask = pd.Series(
        False,
        index=filtered_df.index
    )

    if "In Air" in selected_status:

        status_mask = (
            status_mask
            |
            filtered_df["on_ground"]
            .astype(str)
            .str.lower()
            .isin(
                ["false", "0", "no"]
            )
        )

    if "On Ground" in selected_status:

        status_mask = (
            status_mask
            |
            filtered_df["on_ground"]
            .astype(str)
            .str.lower()
            .isin(
                ["true", "1", "yes"]
            )
        )

    filtered_df = filtered_df[
        status_mask
    ]


if selected_transport:

    filtered_df = filtered_df[
        filtered_df["transport_kind"]
        .astype(str)
        .isin(selected_transport)
    ]


if selected_category:

    filtered_df = filtered_df[
        filtered_df["category"]
        .astype(str)
        .isin(selected_category)
    ]


if selected_time and "is_day" in filtered_df.columns:

    time_mask = pd.Series(
        False,
        index=filtered_df.index
    )

    if "Day" in selected_time:

        time_mask = (
            time_mask
            |
            filtered_df["is_day"]
            .astype(str)
            .str.lower()
            .isin(
                ["true", "1", "yes"]
            )
        )

    if "Night" in selected_time:

        time_mask = (
            time_mask
            |
            filtered_df["is_day"]
            .astype(str)
            .str.lower()
            .isin(
                ["false", "0", "no"]
            )
        )

    filtered_df = filtered_df[
        time_mask
    ]


if selected_date and "weather_time_utc" in filtered_df.columns:

    weather_datetime = pd.to_datetime(
        filtered_df["weather_time_utc"],
        errors="coerce"
    )

    filtered_df = filtered_df[
        weather_datetime.dt.date.isin(
            selected_date
        )
    ]


# =========================================================
# INFO BAR
# =========================================================

active_filters = []


if selected_country:
    active_filters.append(
        f"Country: {len(selected_country)}"
    )

if selected_status:
    active_filters.append(
        f"Status: {len(selected_status)}"
    )

if selected_transport:
    active_filters.append(
        f"Transport: {len(selected_transport)}"
    )

if selected_category:
    active_filters.append(
        f"Category: {len(selected_category)}"
    )

if selected_time:
    active_filters.append(
        f"Time: {len(selected_time)}"
    )

if selected_date:
    active_filters.append(
        f"Date: {len(selected_date)}"
    )


filter_text = (
    " | ".join(active_filters)
    if active_filters
    else "No filters applied"
)


st.markdown(
    f"""
    <div class="info-bar">
        <b>{len(filtered_df):,}</b> weather-linked flight records |
        {filter_text} |
        Source: Gold.flight_weather
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FLIGHT OPERATIONS
# =========================================================

st.markdown(
    '<div class="section-header">✈️ Flight Operations</div>',
    unsafe_allow_html=True
)


# =========================================================
# FILTERED KPI VALUES
# =========================================================

total_flights = filtered_df["flight_id"].nunique()

in_air_count = filtered_df.loc[
    filtered_df["on_ground"].astype(str).str.lower().isin(
        ["false", "0", "no"]
    ),
    "flight_id"
].nunique()

on_ground_count = filtered_df.loc[
    filtered_df["on_ground"].astype(str).str.lower().isin(
        ["true", "1", "yes"]
    ),
    "flight_id"
].nunique()

countries_count = filtered_df["country"].nunique()

avg_altitude = average(
    filtered_df,
    "altitude_m"
)

avg_speed = average(
    filtered_df,
    "velocity_kmh"
)

avg_temperature = average(
    filtered_df,
    "temperature_celsius"
)

avg_wind = average(
    filtered_df,
    "wind_speed_kmh"
)

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.metric(
        "✈️ Total Flights",
        number_format(total_flights)
    )


with k2:

    st.metric(
        "🛫 In Air",
        number_format(in_air_count)
    )


with k3:

    st.metric(
        "🛬 On Ground",
        number_format(on_ground_count)
    )


with k4:

    st.metric(
        "🌍 Countries",
        number_format(countries_count)
    )


k5, k6, k7, k8 = st.columns(4)


with k5:

    st.metric(
        "📏 Avg Altitude",
        f"{decimal_format(avg_altitude, 2)} m"
    )


with k6:

    st.metric(
        "⚡ Avg Speed",
        f"{decimal_format(avg_speed, 2)} km/h"
    )


with k7:

    st.metric(
        "🌡️ Avg Temperature",
        f"{decimal_format(avg_temperature, 2)} °C"
    )


with k8:

    st.metric(
        "💨 Avg Wind",
        f"{decimal_format(avg_wind, 2)} km/h"
    )


# =========================================================
# FLIGHT STATUS + TRANSPORT
# =========================================================

col1, col2 = st.columns(2)


with col1:

    status_data = pd.DataFrame(
        {
            "Status": [
                "In Air",
                "On Ground"
            ],
            "Flights": [
                in_air_count,
                on_ground_count
            ]
        }
    )


    fig = px.pie(
        status_data,
        names="Status",
        values="Flights",
        hole=0.55,
        title="Flight Status"
    )


    st.plotly_chart(
        chart_style(fig, 390),
        use_container_width=True
    )


with col2:

    if "transport_kind" in filtered_df.columns:

        transport_data = (
            filtered_df[
                filtered_df["transport_kind"].notna()
            ]
            .assign(
                transport_kind=lambda x:
                x["transport_kind"].astype(str)
            )
            .groupby(
                "transport_kind"
            )
            .size()
            .reset_index(
                name="Flights"
            )
            .sort_values(
                "Flights",
                ascending=False
            )
        )

    else:

        transport_data = pd.DataFrame()


    if not transport_data.empty:

        fig = px.bar(
            transport_data,
            x="transport_kind",
            y="Flights",
            title="Flights by Transport Type",
            text="Flights"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            chart_style(fig, 390),
            use_container_width=True
        )

    else:

        st.info(
            "Transport type data is not available."
        )


# =========================================================
# SPEED + ALTITUDE
# =========================================================

col1, col2 = st.columns(2)


with col1:

    speed_data = numeric_column(
        filtered_df,
        "velocity_kmh"
    ).dropna()


    if not speed_data.empty:

        fig = px.histogram(
            x=speed_data,
            nbins=30,
            title="Flight Speed Distribution",
            labels={
                "x": "Speed (km/h)",
                "y": "Flights"
            }
        )

        st.plotly_chart(
            chart_style(fig, 390),
            use_container_width=True
        )

    else:

        st.info(
            "Speed data is not available."
        )


with col2:

    altitude_data = numeric_column(
        filtered_df,
        "altitude_m"
    ).dropna()


    if not altitude_data.empty:

        fig = px.histogram(
            x=altitude_data,
            nbins=30,
            title="Flight Altitude Distribution",
            labels={
                "x": "Altitude (m)",
                "y": "Flights"
            }
        )

        st.plotly_chart(
            chart_style(fig, 390),
            use_container_width=True
        )

    else:

        st.info(
            "Altitude data is not available."
        )


# =========================================================
# WEATHER INTELLIGENCE
# =========================================================

st.markdown(
    '<div class="section-header">🌦️ Weather Intelligence</div>',
    unsafe_allow_html=True
)


avg_humidity = average(
    filtered_df,
    "relative_humidity_percentage"
)

avg_visibility = average(
    filtered_df,
    "visibility_m"
)

avg_pressure = average(
    filtered_df,
    "pressure_msl_hpa"
)

avg_uv = average(
    filtered_df,
    "uv_index"
)


w1, w2, w3, w4 = st.columns(4)


with w1:

    st.metric(
        "💧 Avg Humidity",
        f"{decimal_format(avg_humidity, 1)} %"
    )


with w2:

    visibility_km = (
        avg_visibility / 1000
        if avg_visibility is not None
        else None
    )

    st.metric(
        "👁️ Avg Visibility",
        f"{decimal_format(visibility_km, 1)} km"
    )


with w3:

    st.metric(
        "🧭 Avg Pressure",
        f"{decimal_format(avg_pressure, 1)} hPa"
    )


with w4:

    st.metric(
        "☀️ Avg UV Index",
        decimal_format(avg_uv, 1)
    )


# =========================================================
# WEATHER DISTRIBUTIONS
# =========================================================

col1, col2 = st.columns(2)


with col1:

    temperature_data = numeric_column(
        filtered_df,
        "temperature_celsius"
    ).dropna()


    if not temperature_data.empty:

        fig = px.histogram(
            x=temperature_data,
            nbins=25,
            title="Temperature Distribution",
            labels={
                "x": "Temperature (°C)",
                "y": "Records"
            }
        )

        st.plotly_chart(
            chart_style(fig, 390),
            use_container_width=True
        )

    else:

        st.info(
            "Temperature data is not available."
        )


with col2:

    wind_data = numeric_column(
        filtered_df,
        "wind_speed_kmh"
    ).dropna()


    if not wind_data.empty:

        fig = px.histogram(
            x=wind_data,
            nbins=25,
            title="Wind Speed Distribution",
            labels={
                "x": "Wind Speed (km/h)",
                "y": "Records"
            }
        )

        st.plotly_chart(
            chart_style(fig, 390),
            use_container_width=True
        )

    else:

        st.info(
            "Wind speed data is not available."
        )


# =========================================================
# WEATHER RELATIONSHIPS
# =========================================================

col1, col2 = st.columns(2)


with col1:

    scatter_data = filtered_df[
        [
            "temperature_celsius",
            "relative_humidity_percentage"
        ]
    ].copy()


    scatter_data["temperature_celsius"] = pd.to_numeric(
        scatter_data["temperature_celsius"],
        errors="coerce"
    )


    scatter_data["relative_humidity_percentage"] = pd.to_numeric(
        scatter_data["relative_humidity_percentage"],
        errors="coerce"
    )


    scatter_data = scatter_data.dropna()


    if not scatter_data.empty:

        fig = px.scatter(
            scatter_data,
            x="temperature_celsius",
            y="relative_humidity_percentage",
            title="Temperature vs Humidity",
            labels={
                "temperature_celsius": "Temperature (°C)",
                "relative_humidity_percentage": "Humidity (%)"
            }
        )

        st.plotly_chart(
            chart_style(fig, 390),
            use_container_width=True
        )

    else:

        st.info(
            "Temperature and humidity data is not available."
        )


with col2:

    scatter_data = filtered_df[
        [
            "temperature_celsius",
            "wind_speed_kmh"
        ]
    ].copy()


    scatter_data["temperature_celsius"] = pd.to_numeric(
        scatter_data["temperature_celsius"],
        errors="coerce"
    )


    scatter_data["wind_speed_kmh"] = pd.to_numeric(
        scatter_data["wind_speed_kmh"],
        errors="coerce"
    )


    scatter_data = scatter_data.dropna()


    if not scatter_data.empty:

        fig = px.scatter(
            scatter_data,
            x="temperature_celsius",
            y="wind_speed_kmh",
            title="Temperature vs Wind Speed",
            labels={
                "temperature_celsius": "Temperature (°C)",
                "wind_speed_kmh": "Wind Speed (km/h)"
            }
        )

        st.plotly_chart(
            chart_style(fig, 390),
            use_container_width=True
        )

    else:

        st.info(
            "Temperature and wind data is not available."
        )


# =========================================================
# FLIGHT GEOGRAPHY
# =========================================================

st.markdown(
    '<div class="section-header">🌍 Flight Geography</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    if "country" in filtered_df.columns:

        country_data = (
            filtered_df[
                filtered_df["country"].notna()
            ]
            .assign(
                country=lambda x:
                x["country"].astype(str)
            )
            .groupby(
                "country"
            )
            .size()
            .reset_index(
                name="Flights"
            )
            .sort_values(
                "Flights",
                ascending=False
            )
            .head(15)
        )

    else:

        country_data = pd.DataFrame()


    if not country_data.empty:

        fig = px.bar(
            country_data,
            x="country",
            y="Flights",
            title="Top 15 Countries by Flights",
            text="Flights"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            chart_style(fig, 420),
            use_container_width=True
        )

    else:

        st.info(
            "Country data is not available."
        )


with col2:

    if (
        "latitude" in filtered_df.columns
        and
        "longitude" in filtered_df.columns
    ):

        map_data = filtered_df.copy()

        map_data["latitude"] = pd.to_numeric(
            map_data["latitude"],
            errors="coerce"
        )

        map_data["longitude"] = pd.to_numeric(
            map_data["longitude"],
            errors="coerce"
        )

        map_data = map_data.dropna(
            subset=[
                "latitude",
                "longitude"
            ]
        )

    else:

        map_data = pd.DataFrame()


    if not map_data.empty:

        hover_columns = [
            column
            for column in [
                "flight_id",
                "country",
                "airline",
                "origin",
                "destination",
                "altitude_m",
                "velocity_kmh"
            ]
            if column in map_data.columns
        ]


        fig = px.scatter_geo(
            map_data,
            lat="latitude",
            lon="longitude",
            hover_name=(
                "callsign"
                if "callsign" in map_data.columns
                else None
            ),
            hover_data=hover_columns,
            title="Aircraft Locations"
        )


        fig.update_geos(
            bgcolor="#111827",
            showland=True,
            landcolor="#1f2937",
            showcountries=True,
            countrycolor="#475569"
        )


        st.plotly_chart(
            chart_style(fig, 420),
            use_container_width=True
        )

    else:

        st.info(
            "Flight coordinates are not available."
        )


# =========================================================
# AIRPORT ANALYTICS
# =========================================================

st.markdown(
    '<div class="section-header">🛫 Airport Analytics</div>',
    unsafe_allow_html=True
)


if airport_df.empty:

    st.warning(
        "No airport data found in Gold layer."
    )

else:

    if "total_airports" in airport_df.columns:

        total_airports = pd.to_numeric(
            airport_df["total_airports"],
            errors="coerce"
        ).sum()

    else:

        total_airports = 0


    if "total_cities" in airport_df.columns:

        total_cities = pd.to_numeric(
            airport_df["total_cities"],
            errors="coerce"
        ).sum()

    else:

        total_cities = 0


    if "country" in airport_df.columns:

        total_countries = (
            airport_df["country"]
            .dropna()
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .nunique()
        )

    else:

        total_countries = 0


    if "average_elevation_m" in airport_df.columns:

        avg_elevation = pd.to_numeric(
            airport_df["average_elevation_m"],
            errors="coerce"
        ).mean()

    else:

        avg_elevation = None


    if "highest_airport_elevation_m" in airport_df.columns:

        highest_elevation = pd.to_numeric(
            airport_df[
                "highest_airport_elevation_m"
            ],
            errors="coerce"
        ).max()

    else:

        highest_elevation = None


    if "lowest_airport_elevation_m" in airport_df.columns:

        lowest_elevation = pd.to_numeric(
            airport_df[
                "lowest_airport_elevation_m"
            ],
            errors="coerce"
        ).min()

    else:

        lowest_elevation = None


    ak1, ak2, ak3 = st.columns(3)


    with ak1:

        st.metric(
            "🛫 Total Airports",
            number_format(total_airports)
        )


    with ak2:

        st.metric(
            "🌍 Countries",
            number_format(total_countries)
        )


    with ak3:

        st.metric(
            "🏙️ Total Cities",
            number_format(total_cities)
        )


    ak4, ak5, ak6 = st.columns(3)


    with ak4:

        st.metric(
            "⛰️ Avg Elevation",
            f"{decimal_format(avg_elevation, 0)} m"
        )


    with ak5:

        st.metric(
            "🔝 Highest Elevation",
            f"{decimal_format(highest_elevation, 0)} m"
        )


    with ak6:

        st.metric(
            "🔽 Lowest Elevation",
            f"{decimal_format(lowest_elevation, 0)} m"
        )


    if (
        "country" in airport_df.columns
        and
        "total_airports" in airport_df.columns
    ):

        airport_country_chart = airport_df[
            [
                "country",
                "total_airports"
            ]
        ].copy()


        airport_country_chart[
            "total_airports"
        ] = pd.to_numeric(
            airport_country_chart[
                "total_airports"
            ],
            errors="coerce"
        )


        airport_country_chart = (
            airport_country_chart
            .dropna(
                subset=[
                    "country",
                    "total_airports"
                ]
            )
            .sort_values(
                "total_airports",
                ascending=False
            )
            .head(15)
        )


        if not airport_country_chart.empty:

            fig = px.bar(
                airport_country_chart,
                x="country",
                y="total_airports",
                title="Top 15 Countries by Number of Airports",
                text="total_airports"
            )


            fig.update_traces(
                textposition="outside"
            )


            st.plotly_chart(
                chart_style(fig, 420),
                use_container_width=True
            )


    if (
        "country" in airport_df.columns
        and
        "average_elevation_m" in airport_df.columns
    ):

        elevation_chart = airport_df[
            [
                "country",
                "average_elevation_m"
            ]
        ].copy()


        elevation_chart[
            "average_elevation_m"
        ] = pd.to_numeric(
            elevation_chart[
                "average_elevation_m"
            ],
            errors="coerce"
        )


        elevation_chart = (
            elevation_chart
            .dropna(
                subset=[
                    "country",
                    "average_elevation_m"
                ]
            )
            .sort_values(
                "average_elevation_m",
                ascending=False
            )
            .head(15)
        )


        if not elevation_chart.empty:

            fig = px.bar(
                elevation_chart,
                x="country",
                y="average_elevation_m",
                title="Average Airport Elevation by Country",
                text="average_elevation_m"
            )


            fig.update_traces(
                texttemplate="%{text:.0f} m",
                textposition="outside"
            )


            st.plotly_chart(
                chart_style(fig, 420),
                use_container_width=True
            )


    st.markdown(
        "### Airport Summary"
    )


    display_airports = airport_df.copy()


    display_airports = display_airports.rename(
        columns={
            "country": "Country",
            "total_airports": "Total Airports",
            "total_cities": "Total Cities",
            "average_elevation_m":
                "Avg Elevation (m)",
            "highest_airport_elevation_m":
                "Highest Elevation (m)",
            "lowest_airport_elevation_m":
                "Lowest Elevation (m)"
        }
    )


    st.dataframe(
        display_airports,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# FLIGHT DATA EXPLORER
# =========================================================

st.markdown(
    '<div class="section-header">🔎 Flight Data Explorer</div>',
    unsafe_allow_html=True
)


search_term = st.text_input(
    "Search flight records",
    placeholder="Search by Flight ID, ICAO24, Callsign or Country..."
)


explorer_df = filtered_df.copy()


if search_term.strip():

    search_value = search_term.strip().lower()


    searchable_columns = [
        "flight_id",
        "icao24",
        "callsign",
        "country"
    ]


    available_columns = [
        column
        for column in searchable_columns
        if column in explorer_df.columns
    ]


    if available_columns:

        search_mask = pd.Series(
            False,
            index=explorer_df.index
        )


        for column in available_columns:

            search_mask = (
                search_mask
                |
                explorer_df[column]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_value,
                    na=False
                )
            )


        explorer_df = explorer_df[
            search_mask
        ]


st.dataframe(
    explorer_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Flight & Weather Analytics Dashboard |
        PostgreSQL Medallion Architecture |
        Bronze → Silver → Gold
    </div>
    """,
    unsafe_allow_html=True
)