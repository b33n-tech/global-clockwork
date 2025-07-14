# streamlit_app_expanded.py

import streamlit as st
from datetime import datetime
import pytz
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="World Attunement Map - Expanded", layout="wide")

st.title("🌍 World Attunement — Who’s Awake Right Now? (Expanded)")
st.markdown("""
Sync your life with the global rhythm.  
Here's a live look at who's awake, who's dreaming, and where the creative pulse is rising worldwide.
""")

# === TIMEZONE & LOCATION DATA ===
locations = {
    "France (Paris)": "Europe/Paris",
    "UK (London)": "Europe/London",
    "Germany (Berlin)": "Europe/Berlin",
    "Finland (Helsinki)": "Europe/Helsinki",
    "Portugal (Lisbon)": "Europe/Lisbon",
    "Turkey (Istanbul)": "Europe/Istanbul",
    "Russia (Moscow)": "Europe/Moscow",
    "Kenya (Nairobi)": "Africa/Nairobi",
    "South Africa (Johannesburg)": "Africa/Johannesburg",
    "India (Delhi)": "Asia/Kolkata",
    "Pakistan (Karachi)": "Asia/Karachi",
    "Indonesia (Jakarta)": "Asia/Jakarta",
    "China (Beijing)": "Asia/Shanghai",
    "Japan (Tokyo)": "Asia/Tokyo",
    "South Korea (Seoul)": "Asia/Seoul",
    "Singapore": "Asia/Singapore",
    "Philippines (Manila)": "Asia/Manila",
    "Australia (Sydney)": "Australia/Sydney",
    "New Zealand (Auckland)": "Pacific/Auckland",
    "Brazil (São Paulo)": "America/Sao_Paulo",
    "Argentina (Buenos Aires)": "America/Argentina/Buenos_Aires",
    "USA (New York)": "America/New_York",
    "USA (Chicago)": "America/Chicago",
    "USA (Denver)": "America/Denver",
    "USA (San Francisco)": "America/Los_Angeles",
    "Canada (Toronto)": "America/Toronto",
    "Mexico (Mexico City)": "America/Mexico_City",
    "Colombia (Bogotá)": "America/Bogota"
}

# Latitude and longitude for the cities
location_coords = {
    "France (Paris)": (48.8566, 2.3522),
    "UK (London)": (51.5074, -0.1278),
    "Germany (Berlin)": (52.5200, 13.4050),
    "Finland (Helsinki)": (60.1695, 24.9354),
    "Portugal (Lisbon)": (38.7223, -9.1393),
    "Turkey (Istanbul)": (41.0082, 28.9784),
    "Russia (Moscow)": (55.7558, 37.6173),
    "Kenya (Nairobi)": (-1.2921, 36.8219),
    "South Africa (Johannesburg)": (-26.2041, 28.0473),
    "India (Delhi)": (28.6139, 77.2090),
    "Pakistan (Karachi)": (24.8607, 67.0011),
    "Indonesia (Jakarta)": (-6.2088, 106.8456),
    "China (Beijing)": (39.9042, 116.4074),
    "Japan (Tokyo)": (35.6762, 139.6503),
    "South Korea (Seoul)": (37.5665, 126.9780),
    "Singapore": (1.3521, 103.8198),
    "Philippines (Manila)": (14.5995, 120.9842),
    "Australia (Sydney)": (-33.8688, 151.2093),
    "New Zealand (Auckland)": (-36.8485, 174.7633),
    "Brazil (São Paulo)": (-23.5505, -46.6333),
    "Argentina (Buenos Aires)": (-34.6037, -58.3816),
    "USA (New York)": (40.7128, -74.0060),
    "USA (Chicago)": (41.8781, -87.6298),
    "USA (Denver)": (39.7392, -104.9903),
    "USA (San Francisco)": (37.7749, -122.4194),
    "Canada (Toronto)": (43.651070, -79.347015),
    "Mexico (Mexico City)": (19.4326, -99.1332),
    "Colombia (Bogotá)": (4.7110, -74.0721)
}

# Define phase intensities for heatmap
phase_intensity = {
    "🌅 Early Morning": 0.5,
    "☀️ Morning": 0.7,
    "🌞 Midday": 1.0,
    "🌤 Afternoon": 0.9,
    "🌇 Evening": 0.6,
    "🌙 Late Evening": 0.4,
    "🌌 Night / Deep Night": 0.1
}

# Get current time in France as reference
base_time = datetime.now(pytz.timezone("Europe/Paris")).replace(minute=0, second=0, microsecond=0)

# Prepare data list
data = []
for city, tz in locations.items():
    local_dt = base_time.astimezone(pytz.timezone(tz))
    hour = local_dt.hour

    if 5 <= hour < 9:
        phase = "🌅 Early Morning"
    elif 9 <= hour < 12:
        phase = "☀️ Morning"
    elif 12 <= hour < 14:
        phase = "🌞 Midday"
    elif 14 <= hour < 18:
        phase = "🌤 Afternoon"
    elif 18 <= hour < 21:
        phase = "🌇 Evening"
    elif 21 <= hour < 23:
        phase = "🌙 Late Evening"
    else:
        phase = "🌌 Night / Deep Night"

    intensity = phase_intensity.get(phase, 0)
    lat, lon = location_coords[city]

    data.append({
        "City": city,
        "Timezone": tz,
        "Local Time": local_dt.strftime("%H:%M"),
        "Activity Phase": phase,
        "Activity Intensity": intensity,
        "Latitude": lat,
        "Longitude": lon
    })

df = pd.DataFrame(data)

# === Display Table ===
st.subheader("🕒 Local Times & Activity Phases")
st.dataframe(df[["City", "Local Time", "Activity Phase"]].sort_values("Local Time").reset_index(drop=True))

# === Display Map ===
st.subheader("🗺️ Global Activity Heatmap")
fig = px.scatter_geo(
    df,
    lat="Latitude",
    lon="Longitude",
    color="Activity Intensity",
    size="Activity Intensity",
    hover_name="City",
    hover_data=["Local Time", "Activity Phase"],
    color_continuous_scale="YlOrRd",
    projection="natural earth",
    title="World Attunement Heatmap: Who’s Awake Now?"
)
fig.update_layout(geo=dict(showland=True, landcolor="white"))
st.plotly_chart(fig, use_container_width=True)

# === Footer ===
st.markdown("""
---
This dashboard is part of the **World Attunement** lifestyle:  
🌍 Live by global pulses, not clocks.  
🌐 Build, rest, connect — whenever the world is alive.
""")
