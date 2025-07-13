import pandas as pd
import os

# Folder paths
folder_path = "D:/ai-ml/CICIDS/TrafficLabelling"
save_path = "D:/ai-ml/CICIDS/Modified"

# Your attack class mappings
attack_mapping = {
    'BENIGN': 'Normal',
    'DoS Hulk': 'DoS',
    'DoS GoldenEye': 'DoS',
    'DDoS': 'DDoS',
    'PortScan': 'PortScan',
    'Bot': 'Bot',
    'FTP-Patator': 'BruteForce',
    'SSH-Patator': 'BruteForce',
    'Web Attack – Brute Force': 'WebAttack',
    'Web Attack – XSS': 'WebAttack',
    'Web Attack – Sql Injection': 'WebAttack',
    'Infiltration': 'Infiltration',
}

# Create save folder if not exists
os.makedirs(save_path, exist_ok=True)

# Loop over all CSV files
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing: {filename}")

        # Try reading with utf-8, fallback to latin1
        try:
            df = pd.read_csv(file_path, low_memory=False)
        except UnicodeDecodeError:
            print(f"⚡ Encoding issue detected in {filename}, retrying with latin1 encoding...")
            df = pd.read_csv(file_path, encoding='latin1', low_memory=False)

        # Now modify labels
        if ' Label' in df.columns:
            df['Label'] = df[' Label'].map(attack_mapping)
        elif 'Label' in df.columns:
            df['Label'] = df['Label'].map(attack_mapping)
        else:
            print(f"❗ No Label column found in {filename}, skipping...")
            continue

        df = df.dropna(subset=['Label'])

        # Save to modified folder
        save_file = os.path.join(save_path, f"Modified_{filename}")
        df.to_csv(save_file, index=False)
        print(f"✅ Saved: {save_file}")