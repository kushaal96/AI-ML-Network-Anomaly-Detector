import pandas as pd
import joblib
from sklearn.metrics import classification_report

# Load the trained model
model = joblib.load("anomaly_detector.pkl")

# Load the labeled dataset
df = pd.read_csv("labeled_data.csv")

# Drop non-numeric or unnecessary columns (src_ip, dst_ip)
features = df.drop(columns=["anomaly", "src_ip", "dst_ip"], errors="ignore")

# Predict anomalies
df["predicted_anomaly"] = model.predict(features)

# Evaluate model performance
print(classification_report(df["anomaly"], df["predicted_anomaly"]))

# Save the results
df.to_csv("test_results.csv", index=False)
print("Testing complete. Results saved as test_results.csv")
