import pandas as pd

# Load CSV
df = pd.read_csv("Karnataka_tomato.csv")

# Filter only Tomato data
df = df[df["Commodity"].str.lower().str.strip() == "tomato"]

# Save cleaned file
df.to_csv("filtered_tomato.csv", index=False)

print("✅ Filtered Tomato data saved to filtered_tomato.csv")
