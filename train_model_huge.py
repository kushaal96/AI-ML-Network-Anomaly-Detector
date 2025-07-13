# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Step 1: Load the Final Merged Dataset
data = pd.read_csv("D:/ai-ml/CICIDS/Final_CICIDS_Merged.csv")

# Step 2: Handle Missing Values (drop rows with any missing value)
data = data.dropna()

# Step 3: Separate Features and Target
X = data.drop(columns=['Label'])  # Features (all columns except Label)
y = data['Label']                 # Target (Label column)

# Step 4: Split into Train and Test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Initialize and Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 6: Save the Trained Model
joblib.dump(model, "D:/ai-ml/network_traffic_model.pkl")

print("✅ Model trained and saved successfully as 'network_traffic_model.pkl'")
