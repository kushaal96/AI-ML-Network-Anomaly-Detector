import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Load preprocessed data
df = pd.read_csv("processed_data.csv")

# Check packet length distribution
print("Packet Length Min:", df["packet_length"].min())
print("Packet Length Max:", df["packet_length"].max())

# Remove empty & extremely small packets
df = df[(df["packet_length"] > 0.02) & (df["packet_length"] < 1.0)]  
print("After filtering:", df.shape)

# Drop non-numeric features
features = df.drop(columns=["src_ip", "dst_ip"])


# Split into train & test sets
X_train, X_test = train_test_split(features, test_size=0.2, random_state=42)

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler for real-time detection
joblib.dump(scaler, "scaler.pkl")
print("[INFO] Feature scaler saved as 'scaler.pkl'.")

# Train Isolation Forest Model with better contamination rate
model = IsolationForest(n_estimators=150, contamination=0.01, random_state=42)
model.fit(X_train_scaled)

# Predict anomalies
df["anomaly"] = model.predict(scaler.transform(features))
print("Anomaly Label Counts:\n", df["anomaly"].value_counts())

# Save trained model
joblib.dump(model, "anomaly_detector.pkl")
print("[INFO] Model training complete. Saved as 'anomaly_detector.pkl'.")

# Save dataset with anomaly labels
df.to_csv("labeled_data.csv", index=False)
print("[INFO] Labeled data saved as 'labeled_data.csv'.")
