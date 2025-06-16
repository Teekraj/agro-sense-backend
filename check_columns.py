import pandas as pd

# Load the CSV file
df = pd.read_csv("crop_prices_cleaned.csv")

# Normalize column names (strip spaces, lowercase)
df.columns = df.columns.str.strip().str.lower()

# Print all column names
print("Columns:", df.columns.tolist())
