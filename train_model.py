import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib

chunksize = 200000  # Number of rows per chunk
chunks = []

print("✅ Starting to read and preprocess data in chunks...")

# Read CSV file in chunks
for chunk in pd.read_csv("D:/ai-ml/CICIDS/Final_CICIDS_Merged.csv", chunksize=chunksize, low_memory=False):

    # Clean column names
    chunk.columns = chunk.columns.str.strip()

    # Drop irrelevant columns
    columns_to_drop = ['Flow ID', 'Source IP', 'Source Port', 
                       'Destination IP', 'Destination Port', 'Timestamp']
    chunk = chunk.drop(columns=columns_to_drop, errors='ignore')

    # Handle Label column
    if 'Label' not in chunk.columns:
        chunk.rename(columns={" Label": "Label"}, inplace=True)

    chunk = chunk.loc[:, ~chunk.columns.duplicated()]

    # Replace infinite values with NaN
    chunk.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Drop rows with NaN values
    chunk.dropna(inplace=True)

    # Append clean chunk
    chunks.append(chunk)

    print(f"✅ Processed chunk of shape: {chunk.shape}")

# Concatenate all cleaned chunks into one dataframe
data = pd.concat(chunks, ignore_index=True)
print("✅ Final merged dataset shape:", data.shape)

# Encode labels
label_encoder = LabelEncoder()
data['Label'] = label_encoder.fit_transform(data['Label'])

# Features and target
X = data.drop(columns=["Label"])
y = data["Label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

# Train Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Save model to disk
joblib.dump(model, "trained_model.pkl")
print("✅ Model saved as trained_model.pkl")

# Evaluate accuracy on test set
test_accuracy = model.score(X_test, y_test)
print(f"✅ Test Accuracy: {test_accuracy * 100:.2f}%")