# streamlit_app.py

import streamlit as st
from datetime import datetime
import pytz
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="World Attunement Map", layout="wide")

st.title("🌍 World Attunement — Who’s Awake Right Now?")
st.markdown("""
Imagine syncing your life with the global rhythm.  
Here’s a live look at who's awake, who's dreaming, and where the creative pulse is rising.
""")

# === TIMEZONE DATA ===

locations = {
    "France (Paris)": "Europe/Paris",
    "UK (London)": "Europe/London",
    "Finland (Helsinki)": "Europe/Helsinki",
    "Kenya (Nairobi)": "Africa/Nairobi",
    "India (Delhi)": "Asia/Kolkata",
    "China (Beijing)": "Asia/Shanghai",
    "Singapore": "Asia/Singapore",
    "Australia (Sydney)": "Australia/Sydney",
    "Brazil (São Paulo)": "America/Sao_Paulo",
    "USA (New York)": "America/New_York",
    "USA (San Francisco)": "America/Los_Angeles",
    "Canada (Toronto)": "America/Toronto"
}

location_coords = {
    "France (Paris)": (48.8566, 2.3522),
    "UK (London)": (51.5074, -0.1278),
    "Finland (Helsinki)": (60.1695, 24.9354),
    "Kenya (Nairobi)": (-1.2921, 36.8219),
    "India (Delhi)": (28.6139, 77.2090),
    "China (Beijing)": (39.9042, 116.4074),
    "Singapore": (1.3521, 103.8198),
    "Australia (Sydney)": (-33.8688, 151.2093),
    "Brazil (São Paulo)": (-23.5505, -46.6333),
    "USA (New York)": (40.7128, -74.0060),
    "USA (San Francisco)": (37.7749, -122.4194),
    "Canada (Toronto)": (43.651070, -79.347015)
}

phase_intensity = {
    "🌅 Early Morning": 0.5,
    "☀️ Morning": 0.7,
    "🌞 Midday": 1.0,
    "🌤 Afternoon": 0.9,
    "🌇 Evening": 0.6,
    "🌙 Late Evening": 0.4,
    "🌌 Night / Deep Night": 0.1
}

# === PROCESS DATA ===

base_time = datetime.now(pytz.timezone("Europe/Paris")).replace(minute=0, second=0, microsecond=0)

data = []
for location, timezone in locations.items():
    local_time = base_time.astimezone(pytz.timezone(timezone))
    local_hour = local_time.hour
    phase = ""

    if 5 <= local_hour < 9:
        phase = "🌅 Early Morning"
    elif 9 <= local_hour < 12:
        phase = "☀️ Morning"
    elif 12 <= local_hour < 14:
        phase = "🌞 Midday"
    elif 14 <= local_hour < 18:
        phase = "🌤 Afternoon"
    elif 18 <= local_hour < 21:
        phase = "🌇 Evening"
    elif 21 <= local_hour < 23:
        phase = "🌙 Late Evening"
    else:
        phase = "🌌 Night / Deep Night"

    lat, lon = location_coords[location]
    intensity = phase_intensity.get(phase, 0)

    data.append({
        "Location": location,
        "Local Time": local_time.strftime("%H:%M"),
        "Activity Phase": phase,
        "Activity Intensity": intensity,
        "Latitude": lat,
        "Longitude": lon
    })

df = pd.DataFrame(data)

# === DISPLAY TABLE ===

st.subheader("🕒 Current Time Snapshot")
st.dataframe(df[["Location", "Local Time", "Activity Phase"]].sort_values("Local Time").reset_index(drop=True))

# === DISPLAY MAP ===

st.subheader("🗺️ Global Heatmap")
fig = px.scatter_geo(
    df,
    lat="Latitude",
    lon="Longitude",
    color="Activity Intensity",
    size="Activity Intensity",
    hover_name="Location",
    hover_data=["Local Time", "Activity Phase"],
    color_continuous_scale="YlOrRd",
    projection="natural earth",
    title="World Attunement Heatmap: Who’s Awake Now?"
)
fig.update_layout(geo=dict(showland=True, landcolor="white"))
st.plotly_chart(fig, use_container_width=True)

# === FOOTER ===

st.markdown("""
---
This is part of the **World Attunement** lifestyle:  
🌍 Live by global pulses, not clocks.  
🌐 Build, rest, connect — when the world is alive.
""")
