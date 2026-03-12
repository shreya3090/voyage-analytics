import streamlit as st
import requests

st.title("✈️ Voyage Analytics Travel Predictor")

source = st.text_input("Source City")
destination = st.text_input("Destination City")
distance = st.number_input("Distance (km)", min_value=0)
travel_class = st.selectbox("Travel Class", ["Economy", "Business"])

if st.button("Predict Price"):
    
    url = "https://voyage-analytics-api.onrender.com/predict"
    
    data = {
        "source": source,
        "destination": destination,
        "distance_km": distance,
        "travel_class": travel_class
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.success(f"Estimated Price: ₹{response.json()['price']}")
    else:
        st.error("Prediction failed")