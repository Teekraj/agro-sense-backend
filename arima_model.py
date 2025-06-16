import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def predict_arima(df):
    # Set 'date' as index and interpolate missing dates
    df = df.set_index('date')
    df = df.asfreq('D').interpolate()

    # Fit ARIMA model
    model = ARIMA(df['price'], order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=7)

    # Find best and worst predicted prices
    best = max(forecast)
    worst = min(forecast)

    result = []
    for i, price in enumerate(forecast):
        day = df.index[-1] + pd.Timedelta(days=i + 1)
        result.append({
            "date": day.strftime("%Y-%m-%d"),
            "price": round(price / 100, 2),  # Convert to ₹/kg
            "highlight": "green" if price == best else ("red" if price == worst else "blue")
        })

    return result
