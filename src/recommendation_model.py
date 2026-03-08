import pandas as pd
from sklearn.cluster import KMeans
import joblib

# Load users data
data = pd.read_csv("data/users.csv")

# Use age as clustering feature
X = data[["age"]]

# Train clustering model
model = KMeans(n_clusters=3, random_state=42)
model.fit(X)

# Save model
joblib.dump(model, "models/recommendation_model.pkl")

print("Recommendation model trained successfully!")