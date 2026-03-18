import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic

st.set_page_config(
    page_title="Voyage Analytics",
    page_icon="✈️",
    layout="wide"
)

# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>
.main {
background-color: #0E1117;
}

h1, h2, h3 {
color: #4CAF50;
}

.stMetric {
background-color: #1c1f26;
padding: 15px;
border-radius: 10px;
}

.stButton>button {
background-color: #4CAF50;
color: white;
border-radius: 10px;
height: 3em;
width: 100%;
}
</style>
""", unsafe_allow_html=True)

# API URLs
predict_api = "https://voyage-analytics-api-9yde.onrender.com/predict"
recommend_api = "https://voyage-analytics-api-9yde.onrender.com/recommend"
gender_api = "https://voyage-analytics-api-9yde.onrender.com/predict_gender"

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

# Title
st.title("✈️ Voyage Analytics Dashboard")
st.write("AI-Powered Travel Insights Platform")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
"Flight Prediction",
"Route Map",
"Travel Recommendation",
"Analytics",
"Model Insights",
"Hotel Finder"
])

st.subheader("🌍 Explore Popular Destinations")

col1, col2, col3 = st.columns(3)

with col1:
    st.image(
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
        caption="Miami Beaches",
        width="stretch"
    )

with col2:
    st.image(
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
        caption="San Francisco Skyline",
        width="stretch"
    )

with col3:
    st.image(
        "https://images.unsplash.com/photo-1490578474895-699cd4e2cf59",
        caption="New York City",
        width="stretch"
    )

# --------------------------------
# ✈️ TAB 1 – Flight Prediction
# --------------------------------
with tab1:

    st.header("Flight Price Predictor")

    col1, col2 = st.columns(2)

    with col1:
        from_city = st.selectbox("From City", list(city_coordinates.keys()), key="from_city")
        flight_type = st.selectbox("Flight Type", ["firstClass", "economic", "premium"], key="flight_type")

    with col2:
        to_city = st.selectbox("To City", list(city_coordinates.keys()), key="to_city")
        agency = st.selectbox("Airline Agency", ["FlyingDrops", "CloudFy", "Rainbow"], key="agency")

    date = st.date_input("Travel Date", key="date")

    if st.button("Predict Flight Price"):

        if from_city == to_city:
            st.warning("⚠️ Departure and destination cannot be same")
            st.stop()

        data = {
            "from": from_city,
            "to": to_city,
            "flightType": flight_type,
            "agency": agency,
            "date": str(date)
        }

        with st.spinner("✈️ Predicting flight price..."):

            try:
                response = requests.post(predict_api, json=data)
                if response.status_code == 200:
                    result = response.json()
                    price = result.get("predicted_price", 0)
                    distance = result.get("calculated_distance_km", 0)
                    col1, col2 = st.columns(2)
                    col1.metric("💰 Estimated Price", f"${round(price,2)}")
                    col2.metric("📍 Distance", f"{round(distance,2)} km")
                    st.progress(min(int(price/50), 100))
                    st.caption("💡 Higher distance usually increases price")
                    st.success("✅ Prediction Successful")
                else:
                    st.error(f"❌ API Error: {response.text}")
            except Exception as e:
                st.error(f"🚨 Connection Error: {e}")

# --------------------------------
# 🌍 TAB 2 – Flight Map
# --------------------------------
with tab2:

    st.header("Flight Route Visualization")

    from_city = st.selectbox("Departure City", list(city_coordinates.keys()), key="map_from")
    to_city = st.selectbox("Arrival City", list(city_coordinates.keys()), key="map_to")

    coord1 = city_coordinates[from_city]
    coord2 = city_coordinates[to_city]

    map_data = pd.DataFrame({
        "lat": [coord1[0], coord2[0]],
        "lon": [coord1[1], coord2[1]]
    })

    st.map(map_data)

    distance = calculate_distance(from_city, to_city)

    st.info(f"Route Distance: {round(distance,2)} km")

# --------------------------------
# 🎯 TAB 3 – Travel Recommendation
# --------------------------------
with tab3:

    st.header("AI Travel Recommendation")

    age = st.slider("Traveler Age", 15, 70, 25)

    if st.button("Get Recommendation"):

        data = {"age": age}

        response = requests.post(recommend_api, json=data)

        if response.status_code == 200:

            rec = response.json()["recommendation"]

            st.success(f"Recommended Travel Style: {rec}")

        else:
            st.error("Recommendation API failed")

    st.subheader("Gender Prediction")

    if st.button("Predict Gender"):

        data = {"age": age}

        response = requests.post(gender_api, json=data)

        if response.status_code == 200:

            gender = response.json()["predicted_gender"]

            st.info(f"Predicted Gender: {gender}")

        else:
            st.error("Gender API failed")

# --------------------------------
# 📊 TAB 4 – Analytics Dashboard
# --------------------------------
with tab4:

    st.header("Travel Analytics Insights")

    data = pd.DataFrame({
        "Age Group": ["18-25","26-35","36-50","50+"],
        "Beach Trips":[40,30,20,10],
        "Adventure Trips":[35,40,20,5],
        "Luxury Travel":[10,20,40,30]
    })

    st.write("Travel preferences across age groups")

    fig, ax = plt.subplots()

    ax.plot(data["Age Group"], data["Beach Trips"], label="Beach")
    ax.plot(data["Age Group"], data["Adventure Trips"], label="Adventure")
    ax.plot(data["Age Group"], data["Luxury Travel"], label="Luxury")

    ax.set_xlabel("Age Group")
    ax.set_ylabel("Preference Score")
    ax.legend()

    st.pyplot(fig)

    st.subheader("Dataset Preview")
    st.dataframe(data)

    st.subheader("Flight Price Trend")

    trend_data = pd.DataFrame({
        "Month": ["Jan","Feb","Mar","Apr","May","Jun"],
        "Average Price":[320,350,400,380,420,450]
    })

    fig, ax = plt.subplots()
    ax.plot(trend_data["Month"], trend_data["Average Price"], marker="o")

    ax.set_xlabel("Month")
    ax.set_ylabel("Average Flight Price ($)")
    ax.set_title("Flight Price Trend")

    st.pyplot(fig)

    st.subheader("Global Travel Demand Heatmap")

    map_data = pd.DataFrame({
        "lat":[40.71,34.05,41.87,37.77,25.76],
        "lon":[-74.00,-118.24,-87.62,-122.41,-80.19],
        "demand":[100,80,60,70,90]
    })

    st.map(map_data)

# --------------------------------
# 🧠 TAB 5 – Model Insights
# --------------------------------
with tab5:

    st.header("Machine Learning Model Insights")

    st.write("""
    This platform uses machine learning models to predict flight prices
    and generate travel recommendations.
    """)

    importance = pd.DataFrame({
        "Feature":["Distance","Flight Type","Agency","Month"],
        "Importance":[0.45,0.25,0.20,0.10]
    })

    fig, ax = plt.subplots()
    ax.bar(importance["Feature"], importance["Importance"])
    ax.set_title("Feature Importance")

    st.pyplot(fig)

# --------------------------------
# 🏨 TAB 6 – Hotel Finder
# --------------------------------
with tab6:

    # 🌍 Destination Section
    st.subheader("🗺 Choose Your Dream Destination")

    destination = st.selectbox(
        "Select destination",
        ["Miami", "New York", "San Francisco"],
        key="destination_tab6"
    )

    images = {
        "Miami":"https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
        "New York":"https://images.unsplash.com/photo-1490578474895-699cd4e2cf59",
        "San Francisco":"https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"
    }

    captions = {
        "Miami": "🌴 Relax at sunny beaches",
        "New York": "🏙 Explore the city that never sleeps",
        "San Francisco": "🌉 Discover iconic Golden Gate views"
    }

    st.image(images[destination], width="stretch")
    st.caption(captions[destination])

    st.divider()

    # 🤖 AI Assistant
    st.header("🤖 AI Travel Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("Ask something about travel")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        if "beach" in user_input.lower():
            response = "🌴 Visit Miami!"
        elif "cheap" in user_input.lower():
            response = "💡 Book early for cheaper flights!"
        elif "luxury" in user_input.lower():
            response = "👑 Try New York luxury hotels!"
        else:
            response = "✈️ Try flight prediction tab!"

        st.session_state.messages.append({"role": "assistant", "content": response})

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 Assistant:** {msg['content']}")

    st.divider()

    # 🏨 HOTEL SECTION
    st.header("🏨 Hotel Recommendations")

    # Filters
    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox(
            "Select City",
            ["Miami", "New York"],
            key="hotel_city"
        )

    with col2:
        budget = st.selectbox(
            "Budget",
            ["Budget", "Mid Range", "Luxury"],
            key="hotel_budget"
        )

    # Hotel Data
    hotel_data = {
        "Miami": [
            {"name": "The Setai", "price": 450, "rating": 5,
             "img": "https://images.unsplash.com/photo-1566073771259-6a8506099945"},
            {"name": "Loews Miami Beach", "price": 250, "rating": 4,
             "img": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa"},
        ],
        "New York": [
            {"name": "The Plaza", "price": 500, "rating": 5,
             "img": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb"},
            {"name": "Pod Times Square", "price": 120, "rating": 3,
             "img": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267"},
        ]
    }

    # Budget Filter Logic
    def filter_hotels(hotel):
        if budget == "Budget":
            return hotel["price"] <= 200
        elif budget == "Mid Range":
            return 200 < hotel["price"] <= 400
        else:
            return hotel["price"] > 400

    filtered_hotels = [h for h in hotel_data[city] if filter_hotels(h)]

    # Display Hotels
    for i, hotel in enumerate(filtered_hotels):

        with st.container():
            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(hotel["img"], width="stretch")

            with col2:
                st.subheader(hotel["name"])
                st.write("⭐" * hotel["rating"])
                st.write(f"💰 ${hotel['price']}/night")

                if st.button(f"Book Now", key=f"book_{i}"):
                    st.success(f"✅ {hotel['name']} booked!")

    # Budget Info
    if budget == "Budget":
        st.info("💸 Affordable stay with essential amenities.")
    elif budget == "Mid Range":
        st.info("🏨 Comfortable stay with great services.")
    else:
        st.info("👑 Premium luxury experience with top facilities.")
