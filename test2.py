import pandas as pd
df = pd.read_csv("labeled_data.csv")
print(df[df["anomaly"] == -1].sample(10))  # Show 10 random anomalies
