import pandas as pd
import os

# Folder where all modified CSVs are saved
modified_folder = "D:/ai-ml/CICIDS/Modified"

# List all Modified CSVs
csv_files = [f for f in os.listdir(modified_folder) if f.endswith('.csv')]

# Merge all CSVs
merged_df = pd.DataFrame()
for file in csv_files:
    file_path = os.path.join(modified_folder, file)
    temp_df = pd.read_csv(file_path)
    merged_df = pd.concat([merged_df, temp_df], ignore_index=True)

# Save final merged dataset
merged_df.to_csv("D:/ai-ml/CICIDS/Final_CICIDS_Merged.csv", index=False)

print(f"✅ Merged {len(csv_files)} files into Final_CICIDS_Merged.csv")
