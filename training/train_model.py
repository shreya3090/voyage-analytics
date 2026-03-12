import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import root_mean_squared_error
import joblib
import os


def main():

    # -----------------------------
    # Paths
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    data_path = os.path.join(BASE_DIR, "data", "flights.csv")
    model_dir = os.path.join(BASE_DIR, "models")

    os.makedirs(model_dir, exist_ok=True)

    # -----------------------------
    # Load Data
    # -----------------------------
    df = pd.read_csv(data_path)

    # Convert date → month
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["month"] = df["date"].dt.month

    df = df.dropna()

    # -----------------------------
    # Features
    # -----------------------------
    features = ["from", "to", "flightType", "agency", "distance", "month"]
    target = "price"

    X = df[features]
    y = df[target]

    cat_cols = ["from", "to", "flightType", "agency"]

    # -----------------------------
    # Preprocessing
    # -----------------------------
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
        ],
        remainder="passthrough"
    )

    # -----------------------------
    # Pipeline
    # -----------------------------
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(
            n_estimators=200,
            random_state=42,
            n_jobs=-1
        ))
    ])

    # -----------------------------
    # Train / Test Split
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # -----------------------------
    # MLflow
    # -----------------------------
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("Voyage_Analytics_Flight_Price")

    with mlflow.start_run():

        pipeline.fit(X_train, y_train)

        preds = pipeline.predict(X_test)

        rmse = root_mean_squared_error(y_test, preds)

        mlflow.log_param("model", "RandomForest")
        mlflow.log_param("n_estimators", 200)

        mlflow.log_metric("rmse", rmse)

        mlflow.sklearn.log_model(
            pipeline,
            artifact_path="flight_price_model"
        )

        model_path = os.path.join(model_dir, "flight_model.pkl")
        joblib.dump(pipeline, model_path)

    print("✅ Model trained and saved successfully")


if __name__ == "__main__":
    main()