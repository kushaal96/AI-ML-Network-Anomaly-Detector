import pandas as pd

data = pd.read_csv("D:/ai-ml/CICIDS/Final_CICIDS_Merged.csv", nrows=10)
print(data.head())
print(data.columns.tolist())
