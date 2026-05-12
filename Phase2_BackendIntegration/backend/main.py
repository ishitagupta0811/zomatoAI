from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas import RecommendationRequest, RecommendationResponse, RestaurantInfo
from backend.database import get_candidate_restaurants, get_unique_locations, get_unique_cuisines
from backend.ai_service import enrich_with_ai
import uvicorn

app = FastAPI(title="Zomato AI API", description="Backend for Zomato AI Recommendation Engine")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/recommend", response_model=RecommendationResponse)
async def recommend_restaurants(request: RecommendationRequest):
    # Phase 2: Get Candidate Pool from Database
    candidates = get_candidate_restaurants(
        location=request.location,
        budget_max=request.budget_max,
        cuisine=request.cuisine_preference,
        min_rating=request.min_rating,
        limit=15
    )
    
    if not candidates:
        raise HTTPException(status_code=404, detail="No restaurants found matching your criteria. Try loosening your filters.")
        
    # Phase 3: Pass candidates to Groq LLM to generate reasoning
    user_prefs = request.model_dump()
    
    # We only pass the top 5 candidates to the LLM to save tokens and ensure fast responses
    top_candidates = candidates[:5]
    enriched_candidates = enrich_with_ai(top_candidates, user_prefs)
    
    results = []
    for cand in enriched_candidates:
        results.append(RestaurantInfo(
            name=cand["name"],
            location=cand["location"],
            rating=cand["rating"],
            cost_for_two=cand["cost_for_two"],
            cuisines=cand["cuisines"],
            url=cand.get("url"),
            ai_explanation=cand.get("ai_explanation")
        ))
        
    return RecommendationResponse(status="success", results=results)

@app.get("/api/v1/locations")
async def get_locations():
    return {"locations": get_unique_locations()}

@app.get("/api/v1/cuisines")
async def get_cuisines():
    return {"cuisines": get_unique_cuisines()}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
