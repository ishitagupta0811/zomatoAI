import sys
import os

# Add parent directory to path so we can import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_helper_endpoints():
    print("==================================================")
    print("Testing GET /api/v1/locations")
    response = client.get("/api/v1/locations")
    print(f"Status Code: {response.status_code}")
    locs = response.json().get("locations", [])
    print(f"Found {len(locs)} locations. First 3: {locs[:3]}\n")

    print("Testing GET /api/v1/cuisines")
    response = client.get("/api/v1/cuisines")
    print(f"Status Code: {response.status_code}")
    cuisines = response.json().get("cuisines", [])
    print(f"Found {len(cuisines)} cuisines. First 3: {cuisines[:3]}\n")

def test_recommendation_endpoint():
    print("==================================================")
    print("Testing POST /api/v1/recommend")
    
    # Case 1
    print("\n--- Test Case 1: Birthday Party ---")
    req_data = {
        "location": "Indiranagar",
        "budget_max": 4000,
        "cuisine_preference": "North Indian",
        "min_rating": 4.5,
        "additional_context": "Looking for a loud, fun place for a birthday party."
    }
    response = client.post("/api/v1/recommend", json=req_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        results = response.json().get("results", [])
        for i, r in enumerate(results):
            reason = r.get('ai_explanation', '')
            reason = reason.replace('\u20b9', 'Rs.')
            print(f"Result {i+1}: {r['name']} | Rating: {r['rating']} | Cost: {r['cost_for_two']}")
            print(f"AI Reason: {reason}")
    else:
        print(f"Error: {response.json()}")

    # Case 2
    print("\n--- Test Case 2: Healthy Lunch ---")
    req_data = {
        "location": "HSR",
        "budget_max": 800,
        "cuisine_preference": "Healthy Food",
        "min_rating": 4.0,
        "additional_context": "I want a light, healthy lunch option for a work break."
    }
    response = client.post("/api/v1/recommend", json=req_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        results = response.json().get("results", [])
        for i, r in enumerate(results):
            reason = r.get('ai_explanation', '')
            reason = reason.replace('\u20b9', 'Rs.')
            print(f"Result {i+1}: {r['name']} | Rating: {r['rating']} | Cost: {r['cost_for_two']}")
            print(f"AI Reason: {reason}")
    else:
        print(f"Error: {response.json()}")

if __name__ == "__main__":
    test_helper_endpoints()
    test_recommendation_endpoint()
