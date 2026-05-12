from pydantic import BaseModel, Field
from typing import List, Optional

class RecommendationRequest(BaseModel):
    location: str = Field(..., description="The city or location")
    budget_max: int = Field(..., description="Maximum cost for two")
    cuisine_preference: str = Field(..., description="Primary cuisine type")
    min_rating: float = Field(..., description="Minimum acceptable rating")
    additional_context: Optional[str] = Field(None, description="Any additional nuances for the LLM")

class RestaurantInfo(BaseModel):
    name: str
    location: str
    rating: float
    cost_for_two: int
    cuisines: str
    url: Optional[str] = None
    ai_explanation: Optional[str] = None

class RecommendationResponse(BaseModel):
    status: str = "success"
    results: List[RestaurantInfo]
