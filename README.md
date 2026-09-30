<div align="center">

<h1>✈️ Flight & Weather Intelligence Dashboard</h1>

<h3>
End-to-End Data Engineering & Business Intelligence Project
</h3>

<p>
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white">
  <img src="https://img.shields.io/badge/Medallion%20Architecture-Bronze%20%7C%20Silver%20%7C%20Gold-8A2BE2?style=for-the-badge">
</p>

<br>

<p>
<b>Flight Data</b> ✈️
&nbsp;&nbsp;→&nbsp;&nbsp;
<b>Weather Data</b> 🌦️
&nbsp;&nbsp;→&nbsp;&nbsp;
<b>Data Engineering</b> ⚙️
&nbsp;&nbsp;→&nbsp;&nbsp;
<b>Business Intelligence</b> 📊
</p>

</div>

---

<h2>📌 About The Project</h2>

<p>
<b>Flight & Weather Intelligence Dashboard</b> is an end-to-end
data engineering and analytics project designed to collect,
process, transform and visualize flight, airport and weather data.
</p>

<p>
The project follows the <b>Medallion Architecture</b>, where raw
data is stored in the <b>Bronze</b> layer, cleaned and structured
data is maintained in the <b>Silver</b> layer, and dashboard-ready
analytical views are created in the <b>Gold</b> layer.
</p>

<p>
The Gold layer is connected to an interactive
<b>Streamlit + Plotly</b> dashboard that provides flight,
weather, geographic and airport analytics.
</p>

---

<h2>🎯 Project Objectives</h2>

<ul>
<li>✈️ Extract flight data from APIs</li>
<li>🛫 Extract airport information</li>
<li>🌦️ Extract weather information</li>
<li>🐘 Store raw data in PostgreSQL</li>
<li>🥉 Implement a Bronze data layer</li>
<li>🥈 Clean and transform data into a Silver layer</li>
<li>🥇 Create analytical Gold views</li>
<li>🔗 Connect flight and weather data using <code>flight_id</code></li>
<li>📊 Calculate analytical KPIs</li>
<li>🎛️ Create interactive dashboard filters</li>
<li>📈 Visualize flight and weather intelligence</li>
</ul>

---

<h2>🏗️ Architecture</h2>

<div align="center">

<table>
<tr>
<td align="center">

<h3>🌐 APIs</h3>

✈️ Flights<br>
🛫 Airports<br>
🌦️ Weather

</td>

<td>➡️</td>

<td align="center">

<h3>🥉 BRONZE</h3>

Raw API Data<br><br>
PostgreSQL

</td>

<td>➡️</td>

<td align="center">

<h3>🥈 SILVER</h3>

Cleaned Data<br><br>
Structured Tables

</td>

<td>➡️</td>

<td align="center">

<h3>🥇 GOLD</h3>

Analytics<br><br>
KPIs & Views

</td>

<td>➡️</td>

<td align="center">

<h3>📊 DASHBOARD</h3>

Streamlit<br>
Plotly

</td>

</tr>
</table>

</div>

---

<h2>🛠️ Technology Stack</h2>

<table>
<tr>
<th>Technology</th>
<th>Purpose</th>
</tr>

<tr>
<td>🐍 Python</td>
<td>API extraction, data processing and application logic</td>
</tr>

<tr>
<td>🐘 PostgreSQL</td>
<td>Database and analytical data storage</td>
</tr>

<tr>
<td>🧮 SQL</td>
<td>Transformation, aggregation and analytical views</td>
</tr>

<tr>
<td>🐼 Pandas</td>
<td>Data cleaning and analysis</td>
</tr>

<tr>
<td>📊 Streamlit</td>
<td>Interactive dashboard</td>
</tr>

<tr>
<td>📈 Plotly</td>
<td>Interactive data visualization</td>
</tr>

<tr>
<td>🌐 REST APIs</td>
<td>Flight, airport and weather data</td>
</tr>

</table>

---

<h2>🌐 Data Sources</h2>

<h3>✈️ Flight Data</h3>

<p>
Flight information is extracted from the PocketWorld Flights API.
</p>

<pre>
https://pocketworld.org/api/flights
</pre>

<h3>🛫 Airport Data</h3>

<pre>
https://pocketworld.org/api/airports
</pre>

<h3>🌦️ Weather Data</h3>

<p>
Weather information is collected using the Open-Meteo Forecast API.
</p>

<pre>
https://api.open-meteo.com/v1/forecast
</pre>

---

<h2>🥉 Bronze Layer</h2>

<p>
The Bronze layer stores the raw API data with minimal transformation.
It provides the original source data for downstream processing.
</p>

<h3>Bronze Tables</h3>

<pre>
bronze.flightdata
bronze.airportdata
bronze.weatherdata
</pre>

<h3>Bronze Responsibilities</h3>

<ul>
<li>Store raw API data</li>
<li>Preserve source information</li>
<li>Maintain original extracted values</li>
<li>Provide source data for transformation</li>
</ul>

---

<h2>🥈 Silver Layer</h2>

<p>
The Silver layer contains cleaned, typed and structured data.
</p>

<h3>Silver Tables</h3>

<pre>
silver.flights
silver.airports
silver.weather
</pre>

<h3>Processing</h3>

<ul>
<li>Numeric data type conversion</li>
<li>Boolean conversion</li>
<li>Timestamp conversion</li>
<li>Data cleaning</li>
<li>Invalid value handling</li>
<li>Structured relational data</li>
</ul>

---

<h2>🔗 Flight & Weather Relationship</h2>

<div align="center">

<table>
<tr>
<td align="center">

<b>silver.flights</b>

<br><br>

<code>flight_id</code> 🔑<br>
callsign<br>
country<br>
latitude<br>
longitude<br>
altitude<br>
velocity

</td>

<td>
&nbsp;&nbsp;&nbsp; 🔗 <br>
<code>flight_id</code>
&nbsp;&nbsp;&nbsp;
</td>

<td align="center">

<b>silver.weather</b>

<br><br>

<code>weather_id</code> 🔑<br>
<code>flight_id</code> 🔗<br>
temperature<br>
humidity<br>
wind speed<br>
precipitation

</td>
</tr>
</table>

</div>

<p>
Weather records are associated with flight records through
<b><code>flight_id</code></b>, allowing flight activity and weather
conditions to be analyzed together.
</p>

---

<h2>🥇 Gold Layer</h2>

<p>
The Gold layer contains dashboard-ready analytical views.
</p>

<pre>
gold.dashboard_kpis
gold.flight_weather
gold.airline_summary
gold.country_summary
gold.airport_summary
gold.weather_summary
</pre>

<table>
<tr>
<th>View</th>
<th>Purpose</th>
</tr>

<tr>
<td><code>dashboard_kpis</code></td>
<td>Overall flight and weather KPIs</td>
</tr>

<tr>
<td><code>flight_weather</code></td>
<td>Main flight and weather analytical dataset</td>
</tr>

<tr>
<td><code>airline_summary</code></td>
<td>Airline-level flight statistics</td>
</tr>

<tr>
<td><code>country_summary</code></td>
<td>Country-level flight statistics</td>
</tr>

<tr>
<td><code>airport_summary</code></td>
<td>Airport-level statistics</td>
</tr>

<tr>
<td><code>weather_summary</code></td>
<td>Weather-level statistics</td>
</tr>

</table>

---

<h2>📊 Dashboard Preview</h2>

<h3>✈️ Dashboard Overview</h3>

<div align="center">

<img src="image/image1.png" width="95%" alt="Flight Weather Dashboard Overview">

</div>

<br>

<h3>📈 Flight Analytics</h3>

<div align="center">

<img src="image/image2.png" width="95%" alt="Flight Analytics Dashboard">

</div>

<br>

<h3>🌦️ Weather Intelligence</h3>

<div align="center">

<img src="image/image3.png" width="95%" alt="Weather Analytics Dashboard">

</div>

<br>

<h3>🌍 Geography & Airport Analytics</h3>

<div align="center">

<img src="image/image4.png" width="95%" alt="Geography and Airport Analytics Dashboard">

</div>

---

<h2>🎛️ Interactive Filters</h2>

<p>The dashboard provides interactive filters for data exploration:</p>

<table>
<tr>
<td>🌍 <b>Country</b></td>
<td>✈️ <b>Flight Status</b></td>
<td>🚍 <b>Transport Type</b></td>
</tr>

<tr>
<td>🛩️ <b>Aircraft Category</b></td>
<td>🌞 <b>Time of Day</b></td>
<td>📅 <b>Weather Date</b></td>
</tr>
</table>

<p>
Dashboard analytics update according to the selected filters.
</p>

---

<h2>📌 Key Performance Indicators</h2>

<table>
<tr>
<th>KPI</th>
<th>Description</th>
</tr>

<tr>
<td>✈️ Total Flights</td>
<td>Total flight records represented in the analytical dataset</td>
</tr>

<tr>
<td>🛫 Flights In Air</td>
<td>Flights represented as airborne</td>
</tr>

<tr>
<td>🛬 Flights On Ground</td>
<td>Flights represented as being on the ground</td>
</tr>

<tr>
<td>🌍 Countries</td>
<td>Countries represented in the dataset</td>
</tr>

<tr>
<td>📏 Average Altitude</td>
<td>Average aircraft altitude</td>
</tr>

<tr>
<td>⚡ Average Speed</td>
<td>Average aircraft velocity</td>
</tr>

<tr>
<td>🌡️ Average Temperature</td>
<td>Average associated temperature</td>
</tr>

<tr>
<td>💨 Average Wind</td>
<td>Average associated wind speed</td>
</tr>

</table>

---

<h2>✈️ Flight Analytics</h2>

<ul>
<li>Flight status analysis</li>
<li>Flights in air vs flights on ground</li>
<li>Flight speed analysis</li>
<li>Flight altitude analysis</li>
<li>Aircraft category distribution</li>
<li>Transport type distribution</li>
<li>Country-level flight analysis</li>
<li>Airline-level analysis</li>
</ul>

---

<h2>🌦️ Weather Intelligence</h2>

<ul>
<li>🌡️ Temperature</li>
<li>💧 Relative humidity</li>
<li>💨 Wind speed</li>
<li>🧭 Wind direction</li>
<li>🌧️ Precipitation</li>
<li>☁️ Cloud cover</li>
<li>📈 Atmospheric pressure</li>
<li>👁️ Visibility</li>
<li>☀️ UV index</li>
<li>🌞 Day / Night conditions</li>
<li>❄️ Snowfall information</li>
<li>🌦️ Weather codes</li>
</ul>

---

<h2>🛬 Airport Analytics</h2>

<ul>
<li>Total airports</li>
<li>Airport countries</li>
<li>Airport cities</li>
<li>Airport elevation</li>
<li>Highest airport elevation</li>
<li>Lowest airport elevation</li>
</ul>

---

<h2>📂 Project Structure</h2>

<pre>
Flight-ETL-pipeline/
│
├── image/
│   ├── image1.png
│   ├── image2.png
│   ├── image3.png
│   └── image4.png
│
├── dashboard/
│   ├── app.py
│   └── database.py
│
├── load_bronze.py
├── load_silver.py
├── database.py
├── requirements.txt
└── README.md
</pre>

---

<h2>⚙️ Installation</h2>

<h3>1️⃣ Clone Repository</h3>

<pre>
git clone YOUR_GITHUB_REPOSITORY_URL
cd Flight-ETL-pipeline
</pre>

<h3>2️⃣ Create Virtual Environment</h3>

<pre>
python -m venv venv
</pre>

<p><b>Windows:</b></p>

<pre>
venv\Scripts\activate
</pre>

<p><b>macOS / Linux:</b></p>

<pre>
source venv/bin/activate
</pre>

<h3>3️⃣ Install Dependencies</h3>

<pre>
pip install -r requirements.txt
</pre>

---

<h2>🐘 PostgreSQL Setup</h2>

<pre>
CREATE DATABASE flight_weather_db;
</pre>

<p>Create the required schemas:</p>

<pre>
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;
</pre>

<p>
Run the SQL scripts included in the project to create the
Bronze tables, Silver tables and Gold analytical views.
</p>

---

<h2>🔐 Database Configuration</h2>

<p>
Update your PostgreSQL connection information in
<code>database.py</code>.
</p>

<pre>
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "flight_weather_db"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
</pre>

<p>
⚠️ <b>Never commit real passwords, API keys or private credentials
to GitHub.</b>
</p>

---

<h2>▶️ Run Dashboard</h2>

<p>Navigate to the dashboard directory:</p>

<pre>
cd dashboard
</pre>

<p>Run Streamlit:</p>

<pre>
streamlit run app.py
</pre>

<p>The dashboard will normally be available at:</p>

<pre>
http://localhost:8501
</pre>

---

<h2>🔄 End-to-End Pipeline</h2>

<div align="center">

<table>
<tr>
<td align="center"><b>🌐 APIs</b><br><br>Flights<br>Airports<br>Weather</td>
<td>➡️</td>
<td align="center"><b>🥉 Bronze</b><br><br>Raw Data</td>
<td>➡️</td>
<td align="center"><b>🥈 Silver</b><br><br>Cleaned Data</td>
<td>➡️</td>
<td align="center"><b>🥇 Gold</b><br><br>Analytics</td>
<td>➡️</td>
<td align="center"><b>📊 Dashboard</b><br><br>Streamlit</td>
</tr>
</table>

</div>

---

<h2>🧠 Data Engineering Concepts</h2>

<table>
<tr>
<td>REST API Integration</td>
<td>JSON Data Extraction</td>
</tr>

<tr>
<td>Data Cleaning</td>
<td>Data Transformation</td>
</tr>

<tr>
<td>PostgreSQL</td>
<td>SQL Aggregations</td>
</tr>

<tr>
<td>SQL Views</td>
<td>Primary Keys</td>
</tr>

<tr>
<td>Foreign Keys</td>
<td>Relational Data Modeling</td>
</tr>

<tr>
<td>Medallion Architecture</td>
<td>Data Integration</td>
</tr>

<tr>
<td>KPI Development</td>
<td>Business Intelligence</td>
</tr>

<tr>
<td>Interactive Dashboards</td>
<td>Data Visualization</td>
</tr>

</table>

---

<h2>🚀 Future Improvements</h2>

<ul>
<li>⏱️ Automated scheduled data ingestion</li>
<li>🔄 Incremental data loading</li>
<li>✅ Data quality monitoring</li>
<li>📝 Pipeline logging</li>
<li>⚙️ Apache Airflow orchestration</li>
<li>🐳 Docker deployment</li>
<li>☁️ Cloud database deployment</li>
<li>📅 Historical flight analysis</li>
<li>🌦️ Historical weather analysis</li>
<li>🔴 Real-time data refresh</li>
<li>🗺️ Advanced geographic visualizations</li>
</ul>

---

<h2>👨‍💻 Author</h2>

<div align="center">

<h2>Waseem Raja Hussain</h2>

<p>
<b>BS Computer Science</b><br>
Iqra University — Airport Campus
</p>

<p>
🐍 Python &nbsp; • &nbsp;
🧮 SQL &nbsp; • &nbsp;
🐘 PostgreSQL &nbsp; • &nbsp;
⚙️ Data Engineering &nbsp; • &nbsp;
📊 Data Analytics &nbsp; • &nbsp;
📈 Business Intelligence
</p>

</div>

---

<div align="center">

<h2>✈️ From Raw APIs → Data Engineering → Analytics → Business Intelligence</h2>

<p>
⭐ <b>If you find this project useful, consider giving the repository a star.</b>
</p>

</div>
