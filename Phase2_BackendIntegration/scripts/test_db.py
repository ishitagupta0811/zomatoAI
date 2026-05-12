import sys
import os

# Add parent directory to path so we can import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import get_candidate_restaurants, get_unique_locations, get_unique_cuisines

def main():
    print("--- Testing Unique Locations ---")
    locs = get_unique_locations()
    print(f"Found {len(locs)} top locations. First 5: {locs[:5]}")
    
    print("\n--- Testing Unique Cuisines ---")
    cuisines = get_unique_cuisines()
    print(f"Found {len(cuisines)} unique cuisines. First 10: {cuisines[:10]}")
    
    print("\n--- Testing Candidate Search ---")
    # Let's search for Italian in Bangalore, < 1500 budget, >= 4.0 rating
    loc = "Koramangala"
    budget = 1500
    cuisine = "Italian"
    min_rating = 4.0
    print(f"Searching: Location={loc}, Budget<={budget}, Cuisine={cuisine}, MinRating={min_rating}")
    
    candidates = get_candidate_restaurants(
        location=loc,
        budget_max=budget,
        cuisine=cuisine,
        min_rating=min_rating,
        limit=5
    )
    
    print(f"Found {len(candidates)} candidates:")
    for c in candidates:
        print(f" - {c['name']} ({c['location']}) | Rating: {c['rating']} | Cost: {c['cost_for_two']} | Cuisines: {c['cuisines']}")

if __name__ == "__main__":
    main()
