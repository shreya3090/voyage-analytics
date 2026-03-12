import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error
import os

# Ensure models folder exists
os.makedirs("models", exist_ok=True)

# Load dataset
df = pd.read_csv("data/flights.csv")

# Convert date
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month

df = df.dropna()

# Encode categorical columns
categorical_cols = ["from", "to", "flightType", "agency"]

encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Features & Target
X = df[["from", "to", "flightType", "agency", "distance", "month"]]
y = df["price"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, pred))

# Save model
joblib.dump(model, "models/flight_model.pkl")
joblib.dump(encoders, "models/flight_encoders.pkl")

print("Flight model saved successfully!")