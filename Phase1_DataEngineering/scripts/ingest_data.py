import sqlite3
import pandas as pd
from datasets import load_dataset
import re

def clean_rate(rate_str):
    if pd.isna(rate_str):
        return None
    rate_str = str(rate_str).strip()
    if rate_str == 'NEW' or rate_str == '-':
        return None
    # Usually rate is like "4.1/5" or "4.1 /5"
    match = re.search(r'^([0-9\.]+)', rate_str)
    if match:
        return float(match.group(1))
    return None

def clean_cost(cost_str):
    if pd.isna(cost_str):
        return None
    cost_str = str(cost_str).replace(',', '').strip()
    try:
        return int(cost_str)
    except ValueError:
        return None

def main():
    print("Downloading/Loading dataset from Hugging Face...")
    dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
    df = dataset.to_pandas()

    print(f"Original dataset size: {len(df)}")

    # Select relevant columns
    cols_to_keep = {
        'name': 'name',
        'location': 'location',
        'approx_cost(for two people)': 'cost_for_two',
        'rate': 'rating',
        'votes': 'votes',
        'cuisines': 'cuisines',
        'url': 'url'
    }
    
    df = df[list(cols_to_keep.keys())].rename(columns=cols_to_keep)

    print("Cleaning data...")
    # Clean rating
    df['rating'] = df['rating'].apply(clean_rate)
    
    # Clean cost
    df['cost_for_two'] = df['cost_for_two'].apply(clean_cost)
    
    # Drop rows without critical info
    df = df.dropna(subset=['name', 'location', 'rating', 'cost_for_two', 'cuisines'])
    
    # Add an ID column
    df.insert(0, 'id', df.index.astype(str))

    print(f"Cleaned dataset size: {len(df)}")
    
    # Save to SQLite
    db_path = "restaurants.db"
    print(f"Saving to {db_path}...")
    
    # Create SQLite connection
    conn = sqlite3.connect(db_path)
    
    # Write to table
    df.to_sql('restaurants', conn, if_exists='replace', index=False)
    
    # Create indexes for fast querying
    cursor = conn.cursor()
    print("Creating indexes...")
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_location ON restaurants (location)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_rating ON restaurants (rating)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cost ON restaurants (cost_for_two)')
    conn.commit()
    conn.close()
    
    print("Data ingestion and engineering complete!")

if __name__ == "__main__":
    main()
