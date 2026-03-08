import streamlit as st
import pandas as pd
import joblib
from geopy.distance import geodesic

# Load model
model = joblib.load("models/flight_model.pkl")

# City coordinates
city_coordinates = {
    "New York": (40.7128, -74.0060),
    "Chicago": (41.8781, -87.6298),
    "Los Angeles": (34.0522, -118.2437),
    "San Francisco": (37.7749, -122.4194),
    "Miami": (25.7617, -80.1918)
}

def calculate_distance(city1, city2):
    coord1 = city_coordinates[city1]
    coord2 = city_coordinates[city2]
    return geodesic(coord1, coord2).km


st.title("✈️ Voyage Analytics")
st.subheader("Flight Price Prediction")

# User inputs
from_city = st.selectbox("From City", list(city_coordinates.keys()))
to_city = st.selectbox("To City", list(city_coordinates.keys()))

flight_type = st.selectbox(
    "Flight Type",
    ["firstClass", "economic", "premium"]
)

agency = st.selectbox(
    "Agency",
    ["FlyingDrops", "CloudFy", "Rainbow"]
)

date = st.date_input("Travel Date")

if st.button("Predict Price"):

    distance = calculate_distance(from_city, to_city)

    df = pd.DataFrame([{
        "from": from_city,
        "to": to_city,
        "flightType": flight_type,
        "agency": agency,
        "distance": distance,
        "month": date.month
    }])

    prediction = model.predict(df)[0]

    st.success(f"Predicted Flight Price: ${round(prediction,2)}")
    st.write(f"Distance: {round(distance,2)} km")