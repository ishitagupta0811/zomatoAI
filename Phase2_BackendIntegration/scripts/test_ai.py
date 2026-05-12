import sys
import os

# Add parent directory to path so we can import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import get_candidate_restaurants
from backend.ai_service import enrich_with_ai

def run_test_case(test_name: str, location: str, budget: int, cuisine: str, min_rating: float, context: str):
    print(f"\n{'='*50}")
    print(f"TEST CASE: {test_name}")
    print(f"{'='*50}")
    print(f"Filters -> Loc: {location} | Budget: <={budget} | Cuisine: {cuisine} | Min Rating: {min_rating}")
    print(f"Context -> {context}\n")
    
    # 1. Fetch from Database
    print("Fetching candidates from SQLite DB...")
    candidates = get_candidate_restaurants(
        location=location,
        budget_max=budget,
        cuisine=cuisine,
        min_rating=min_rating,
        limit=5
    )
    
    if not candidates:
        print("-> 0 Candidates found matching hard filters. Test skipped.")
        return
        
    print(f"-> Found {len(candidates)} candidates.")
    for c in candidates:
         print(f"   - {c['name']} (Rating: {c['rating']}, Cost: {c['cost_for_two']})")
         
    # 2. Enrich with Groq LLM
    print("\nCalling Groq LLM for reasoning...")
    user_prefs = {
        "location": location,
        "budget_max": budget,
        "cuisine_preference": cuisine,
        "min_rating": min_rating,
        "additional_context": context
    }
    
    enriched = enrich_with_ai(candidates, user_prefs)
    
    print("\n--- LLM RECOMMENDATIONS & REASONING ---")
    for r in enriched:
        print(f"Restaurant: {r['name']}")
        reason = r.get('ai_explanation', 'No reasoning generated.')
        # Handle Windows terminal charmap errors with the Rupee symbol
        reason = reason.replace('\u20b9', 'Rs.')
        print(f"AI Reason:  {reason}")
        print("-" * 40)

def main():
    # Test Case 1: Romantic Date Night
    run_test_case(
        test_name="Romantic Anniversary Dinner",
        location="Indiranagar",
        budget=2500,
        cuisine="Italian",
        min_rating=4.2,
        context="I want a quiet, romantic place for an anniversary dinner with great dessert options."
    )
    
    # Test Case 2: Budget Friendly & Fast
    run_test_case(
        test_name="Quick Budget Bite",
        location="Koramangala 5th Block",
        budget=500,
        cuisine="North Indian",
        min_rating=3.5,
        context="Looking for a very cheap, quick bite to eat after work. Ambience doesn't matter, just good spicy food."
    )
    
    # Test Case 3: Family Outing
    run_test_case(
        test_name="Family Buffet",
        location="BTM",
        budget=3000,
        cuisine="North Indian",
        min_rating=4.0,
        context="Taking my extended family out for dinner. Need a place with good portions, family-friendly vibe, and preferably a buffet."
    )

if __name__ == "__main__":
    main()
