import requests

url = "http://127.0.0.1:8000/predict"

data = {
    "from": "Rio de Janeiro (RJ)",
    "to": "Sao Paulo (SP)",
    "flightType": "economic",
    "agency": "CloudFy",
    "distance": 430,
    "date": "2026-04-10"
}

response = requests.post(url, json=data)

print(response.json())