import pandas as pd
import os

# -------------------------------
# Step 1: Load JSON File
# -------------------------------
file_path = "data/trends_20260404.json"   # change filename if needed

try:
    df = pd.read_json(file_path)
    print(f"Loaded {len(df)} stories from {file_path}")
except Exception as e:
    print("Error loading file:", e)
    exit()

# -------------------------------
# Step 2: Clean the Data
# -------------------------------

# Remove duplicates
df = df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {len(df)}")

# Remove missing values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Remove extra whitespace in title
df["title"] = df["title"].str.strip()

# -------------------------------
# Step 3: Save as CSV
# -------------------------------
os.makedirs("data", exist_ok=True)

output_file = "data/trends_clean.csv"

try:
    df.to_csv(output_file, index=False)
    print(f"\nSaved {len(df)} rows to {output_file}")
except Exception as e:
    print("Error saving CSV:", e)


print("\nStories per category:")
print(df["category"].value_counts())


import pandas as pd
import os

# Load JSON
df = pd.read_json("data/trends_20260404.json")
print("Loaded:", len(df))

# Clean data
df = df.drop_duplicates(subset=["post_id"])
print("After duplicates:", len(df))

df = df.dropna(subset=["post_id", "title", "score"])
print("After nulls:", len(df))

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

df = df[df["score"] >= 5]
print("After low scores:", len(df))

df["title"] = df["title"].str.strip()

# Save CSV
os.makedirs("data", exist_ok=True)
df.to_csv("data/trends_clean.csv", index=False)

print("Saved:", len(df))

# Category summary
print(df["category"].value_counts())