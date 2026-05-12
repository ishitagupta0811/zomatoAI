import sqlite3
import os
from typing import List, Dict, Any

# Determine the absolute path to the database relative to this script
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "restaurants.db")

def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run Phase 1 ingestion first.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_candidate_restaurants(location: str, budget_max: int, cuisine: str, min_rating: float, limit: int = 15) -> List[Dict[str, Any]]:
    """
    Fetch a Candidate Pool of restaurants matching the hard filters.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # We use LIKE for location and cuisine to handle partial matches
    query = """
        SELECT name, location, rating, cost_for_two, cuisines, url
        FROM restaurants 
        WHERE location LIKE ? 
          AND cuisines LIKE ? 
          AND cost_for_two <= ? 
          AND rating >= ?
        GROUP BY name
        ORDER BY rating DESC
        LIMIT ?
    """
    
    location_param = f"%{location}%"
    cuisine_param = f"%{cuisine}%"
    
    cursor.execute(query, (location_param, cuisine_param, budget_max, min_rating, limit))
    rows = cursor.fetchall()
    
    candidates = []
    for row in rows:
        candidates.append({
            "name": row["name"],
            "location": row["location"],
            "rating": row["rating"],
            "cost_for_two": row["cost_for_two"],
            "cuisines": row["cuisines"],
            "url": row["url"]
        })
        
    conn.close()
    return candidates

def get_unique_locations() -> List[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT location, count(*) as cnt 
        FROM restaurants 
        GROUP BY location 
        ORDER BY cnt DESC 
        LIMIT 50
    """)
    rows = cursor.fetchall()
    conn.close()
    return [row["location"] for row in rows]

def get_unique_cuisines() -> List[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cuisines FROM restaurants WHERE cuisines IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()
    
    cuisine_set = set()
    for row in rows:
        parts = [c.strip() for c in row["cuisines"].split(",")]
        for p in parts:
            if p:
                cuisine_set.add(p)
                
    return sorted(list(cuisine_set))
