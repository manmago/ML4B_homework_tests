import streamlit as st
import pandas as pd

set_downsample = 50
DOWNSAMPLE = set_downsample

st.set_page_config(page_title="Lecture 2 Task", layout="wide")
st.header("Lecture 2 task")
st.write("A simple streamlit app with data from SensorLogger app and interactive element.")
st.write("Downsampling rate set to: " + str(DOWNSAMPLE))

sensor_options = {
    "Accelerometer": "./data/Accelerometer.csv",
    "Gyroscope": "./data/Gyroscope.csv",
    "Barometer": "./data/Barometer.csv",
    "Total Acceleration": "./data/TotalAcceleration.csv"
}

selected_sensor = st.selectbox(
    "Select Sensor to View", 
    options=sensor_options.keys()
)

# Load selected CSV
@st.cache_data
def load_data(filename):
    return pd.read_csv(filename)

df = load_data(sensor_options[selected_sensor])

# Downsample: keep every nth value (e.g., every 10th point)
downsample_rate = DOWNSAMPLE  # Adjust based on your data frequency
df_downsampled = df.iloc[::downsample_rate]

try:
    if selected_sensor == "Barometer":
        st.line_chart(df_downsampled.set_index('time')[['seconds_elapsed', 'relativeAltitude', 'pressure']])
    else:
        st.line_chart(df_downsampled.set_index('time')[['x', 'y', 'z']])

except FileNotFoundError:
    st.error(f"Could not find {sensor_options[selected_sensor]}")
    st.write("Make sure CSV files are in the same directory as this script")
