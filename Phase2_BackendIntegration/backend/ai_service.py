import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
# We are currently in backend/, so .env is in the root (../..)
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path=env_path)

# Initialize Groq client
# The client automatically looks for the GROQ_API_KEY environment variable
try:
    client = Groq()
except Exception as e:
    print(f"Warning: Failed to initialize Groq client. Ensure GROQ_API_KEY is set. Error: {e}")
    client = None

def enrich_with_ai(candidate_pool: list, user_preferences: dict) -> list:
    """
    Takes a candidate pool of restaurants and user preferences, 
    and uses Groq to generate reasoning for why they match.
    """
    if not client:
        print("Groq client not initialized. Returning mock explanations.")
        return _mock_explanations(candidate_pool)
        
    if not candidate_pool:
        return []

    # Simplify the candidate pool for the prompt to save tokens
    simple_candidates = []
    for c in candidate_pool:
        simple_candidates.append({
            "name": c["name"],
            "rating": c["rating"],
            "cost_for_two": c["cost_for_two"],
            "cuisines": c["cuisines"]
        })

    candidates_str = json.dumps(simple_candidates, indent=2)
    
    system_prompt = (
        "You are ZomatoAI, an expert food critic and personalized dining assistant. "
        "Your goal is to review a provided list of candidate restaurants and evaluate how well they "
        "match the user's specific request. Provide a compelling, 1-2 sentence explanation "
        "for WHY each restaurant is a perfect fit, especially considering any 'additional_context' provided by the user.\n\n"
        "Return the output as a valid JSON object with a single key 'recommendations' containing an array. "
        "Each object in the array MUST have EXACTLY these two keys:\n"
        "- 'name': The exact name of the restaurant.\n"
        "- 'ai_explanation': Your 1-2 sentence personalized explanation.\n"
    )
    
    user_prompt = (
        f"User Preferences: {json.dumps(user_preferences, indent=2)}\n\n"
        f"Candidate Restaurants:\n{candidates_str}\n\n"
        "Generate the JSON object with explanations for these candidates."
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        
        response_content = chat_completion.choices[0].message.content
        ai_data = json.loads(response_content)
        ai_recommendations = ai_data.get("recommendations", [])
        
        # Merge the AI explanations back into the candidate pool
        ai_map = {item["name"]: item.get("ai_explanation", "") for item in ai_recommendations}
        
        enriched_pool = []
        for cand in candidate_pool:
            # If AI didn't return an explanation, provide a fallback
            explanation = ai_map.get(cand["name"], "This restaurant perfectly matches your budget and location preferences.")
            cand_copy = cand.copy()
            cand_copy["ai_explanation"] = explanation
            enriched_pool.append(cand_copy)
            
        return enriched_pool

    except Exception as e:
        print(f"Error during Groq API call: {e}")
        return _mock_explanations(candidate_pool)

def _mock_explanations(candidate_pool):
    """Fallback if API fails or key is missing."""
    enriched = []
    for cand in candidate_pool:
        c = cand.copy()
        c["ai_explanation"] = f"[No API Key] {c['name']} is a great choice for {c['cuisines']} in {c['location']}."
        enriched.append(c)
    return enriched
