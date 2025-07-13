import pandas as pd

# Load the training data
df = pd.read_csv("labeled_data.csv")

# Print feature names (excluding target column)
feature_columns = df.drop(columns=["anomaly"], errors="ignore").columns
print("Feature Order Used in Training:", list(feature_columns))
