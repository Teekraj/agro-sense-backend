from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)

# Load and clean dataset
df = pd.read_csv("crop_prices_cleaned.csv")
df.columns = df.columns.str.strip()

print("✅ Starting backend...")
print("📄 Columns:", list(df.columns))

# Rename columns for consistency
if "Commodity" in df.columns:
    df.rename(columns={"Commodity": "Crop"}, inplace=True)
if "Modal Price" in df.columns:
    df.rename(columns={"Modal Price": "Price"}, inplace=True)
if "Price Date" in df.columns:
    df.rename(columns={"Price Date": "Date"}, inplace=True)

df['Crop'] = df['Crop'].astype(str).str.strip()
df['State'] = "Karnataka"
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date', 'Price'])

# ✅ Predict prices
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    crop = data.get('crop', '').strip()
    state = data.get('state', '').strip()
    district = data.get('district', '').strip()
    market = data.get('market', '').strip()

    if not crop or not district or not market:
        return jsonify({"error": "Missing parameters"}), 400

    # Normalize inputs
    crop = crop.lower().capitalize()
    district = district.lower().capitalize()
    market = market.lower().capitalize()

    # Filter data
    filtered = df[
        (df['Crop'].str.lower().str.strip() == crop.lower()) &
        (df['District'].str.lower().str.strip() == district.lower()) &
        (df['Market'].str.lower().str.strip() == market.lower())
    ]

    if filtered.empty:
        return jsonify([])

    filtered = filtered.sort_values(by='Date').tail(30)
    ts = filtered[['Date', 'Price']].set_index('Date').asfreq('D').interpolate()

    try:
        model = ARIMA(ts['Price'], order=(5, 1, 0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=7)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    result = [
        {"date": d.strftime('%Y-%m-%d'), "price": round(p / 100, 2)}  # ₹ per KG
        for d, p in zip(forecast.index, forecast.values)
    ]
    return jsonify(result)

# ✅ Send district + market combos
@app.route("/locations", methods=["GET"])
def locations():
    locs = df.groupby("District")["Market"].unique().reset_index()
    locs_dict = {
        row["District"]: list(row["Market"]) for _, row in locs.iterrows()
    }
    return jsonify(locs_dict)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
