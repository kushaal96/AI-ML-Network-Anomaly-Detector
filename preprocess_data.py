import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Load the dataset
df = pd.read_csv("network_features.csv")

# Drop duplicate entries
df = df.drop_duplicates()

# Handle missing values (if any)
df = df.dropna()

# Encode categorical columns (IP Addresses & Protocol)
encoder = LabelEncoder()
df["src_ip"] = encoder.fit_transform(df["src_ip"])
df["dst_ip"] = encoder.fit_transform(df["dst_ip"])
df["protocol"] = encoder.fit_transform(df["protocol"])

# Normalize numerical columns (Packet Length & Timestamp)
scaler = MinMaxScaler()
df[["packet_length", "timestamp"]] = scaler.fit_transform(df[["packet_length", "timestamp"]])

# Save the cleaned dataset
df.to_csv("processed_data.csv", index=False)
print("Data preprocessing complete. Saved as processed_data.csv")