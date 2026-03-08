from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd

app = FastAPI()

# Load models
flight_model = joblib.load("flight_model.pkl")
recommendation_model = joblib.load("recommendation_model.pkl")
gender_model = joblib.load("gender_model.pkl")


class FlightRequest(BaseModel):
    from_: str = Field(alias="from")
    to: str
    flightType: str
    agency: str
    date: str


class RecommendRequest(BaseModel):
    age: int


class GenderRequest(BaseModel):
    age: int


valid_flight_types = ["firstClass", "economic", "premium"]
valid_agencies = ["FlyingDrops", "CloudFy", "Rainbow"]
from geopy.distance import geodesic

city_coordinates = {
    "New York": (40.7128, -74.0060),
    "Chicago": (41.8781, -87.6298),
    "Los Angeles": (34.0522, -118.2437),
    "San Francisco": (37.7749, -122.4194),
    "Miami": (25.7617, -80.1918)
}

def calculate_distance(city1, city2):
    coord1 = city_coordinates.get(city1)
    coord2 = city_coordinates.get(city2)

    if coord1 is None or coord2 is None:
        raise ValueError("City not supported")

    return geodesic(coord1, coord2).km

@app.get("/")
def home():
    return {"status": "Voyage Analytics Flight Price API Running!"}


# ✈️ Flight Price Prediction
@app.post("/predict")
def predict(data: FlightRequest):

    if data.flightType not in valid_flight_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid flightType. Allowed: {valid_flight_types}"
        )

    if data.agency not in valid_agencies:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid agency. Allowed: {valid_agencies}"
        )

    try:

        distance = calculate_distance(data.from_, data.to)

        df = pd.DataFrame([{
            "from": data.from_,
            "to": data.to,
            "flightType": data.flightType,
            "agency": data.agency,
            "distance": distance,
            "month": pd.to_datetime(data.date).month
        }])

        prediction = flight_model.predict(df)[0]

        return {
            "predicted_price": float(prediction),
            "calculated_distance_km": distance
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🌍 Travel Recommendation
@app.post("/recommend")
def recommend(data: RecommendRequest):

    cluster = recommendation_model.predict([[data.age]])[0]

    if cluster == 0:
        rec = "Beach Destinations"
    elif cluster == 1:
        rec = "Adventure Trips"
    else:
        rec = "Luxury Travel"

    return {"recommendation": rec}


# 👤 Gender Prediction
@app.post("/predict_gender")
def predict_gender(data: GenderRequest):

    prediction = gender_model.predict([[data.age]])[0]

    return {"predicted_gender": prediction}