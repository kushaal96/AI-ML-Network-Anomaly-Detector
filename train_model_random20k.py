import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# 1. Load data
data = pd.read_csv("D:/ai-ml/CICIDS/Final_CICIDS_Merged.csv")

print(f"Original dataset shape: {data.shape}")

# 2. Sample only 200,000 rows (you can adjust)
data_sampled = data.sample(n=200000, random_state=42)

print(f"Sampled dataset shape: {data_sampled.shape}")

# 3. Split into features (X) and labels (y)
X = data_sampled.drop(columns=["Label"])  # All columns except 'Label'
y = data_sampled["Label"]

# 4. Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Save the trained model
joblib.dump(model, "D:/ai-ml/CICIDS/network_traffic_model.pkl")

print("✅ Model trained and saved successfully!")
