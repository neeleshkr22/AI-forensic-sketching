"""Quick test script for search endpoint"""
import requests
import json

# Test search with JSON (no file)
url = "http://localhost:5000/api/sketch/search"

# Test with mock data
data = {
    "sketch_url": "test.png",
    "top_k": 5,
    "threshold": 0.5
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
