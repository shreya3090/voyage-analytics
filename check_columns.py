import pandas as pd

df = pd.read_csv("data/flights.csv")

print("COLUMNS:")
print(df.columns)

print("\nUNIQUE VALUES IN EACH COLUMN:\n")

for col in df.columns:
    print(f"{col} -> {df[col].unique()[:5]}")