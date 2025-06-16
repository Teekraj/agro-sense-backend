import requests

url = "http://127.0.0.1:5000/predict"
payload = {
    "crop": "Tomato",
    "state": "Karnataka",
    "district": "Belgaum",
    "market": "Belgaum",
    "from_date": "2023-01-01",
    "to_date": "2023-12-31"
}

res = requests.post(url, json=payload)
print(res.status_code)
print(res.json())
