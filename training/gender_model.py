import pandas as pd
import os
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# dataset path
current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "..", "data", "users.csv")

data = pd.read_csv(data_path)

# Features and target
X = data[["age"]]
y = data["gender"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("Gender_Classification")

with mlflow.start_run():

    model = RandomForestClassifier()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    acc = accuracy_score(y_test, predictions)

    mlflow.log_param("model", "RandomForestClassifier")
    mlflow.log_metric("accuracy", acc)

    mlflow.sklearn.log_model(model, "gender_model")

    joblib.dump(model, "models/gender_model.pkl")

print("Model Accuracy:", acc)