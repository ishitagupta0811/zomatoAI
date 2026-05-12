from datasets import load_dataset
import pandas as pd

print("Loading dataset...")
dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation")

print("\nDataset Info:")
print(dataset)

if 'train' in dataset:
    df = dataset['train'].to_pandas()
    print("\nColumns:", df.columns.tolist())
    print("\nData Types:\n", df.dtypes)
    print("\nFirst 5 rows:\n", df.head())
