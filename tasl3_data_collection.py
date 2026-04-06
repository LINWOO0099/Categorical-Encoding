"""
TrendPulse — Task 3: Analysis with Pandas & NumPy
Loads the cleaned CSV from Task 2, explores the data, computes
statistics using NumPy, adds derived columns, and saves the result.
"""

import pandas as pd
import numpy as np
import os

# ── 1. Load and Explore ───────────────────────────────────────────────────────

df = pd.read_csv("data/trends_clean.csv")

print(f"Loaded data: {df.shape}")          # (rows, columns)
print("\nFirst 5 rows:")
print(df.head())

# Round to whole numbers for clean display; scores/comments are integers
avg_score    = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

# ── 2. NumPy Statistics ───────────────────────────────────────────────────────

scores = df["score"].to_numpy()           # Convert to NumPy array once

mean_score   = np.mean(scores)
median_score = np.median(scores)
std_score    = np.std(scores)
max_score    = np.max(scores)
min_score    = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:,.0f}")
print(f"Median score : {median_score:,.0f}")
print(f"Std deviation: {std_score:,.0f}")
print(f"Max score    : {max_score:,.0f}")
print(f"Min score    : {min_score:,.0f}")

# Category with the most stories — value_counts() returns sorted descending
top_category       = df["category"].value_counts().idxmax()
top_category_count = df["category"].value_counts().max()
print(f"\nMost stories in: {top_category} ({top_category_count} stories)")

# Story with the highest comment count
most_commented_idx   = df["num_comments"].idxmax()
most_commented_title = df.loc[most_commented_idx, "title"]
most_commented_count = df.loc[most_commented_idx, "num_comments"]
print(f'\nMost commented story: "{most_commented_title}"  — {most_commented_count:,} comments')

# ── 3. Add New Columns ────────────────────────────────────────────────────────

# engagement: how much discussion a story generates per upvote.
# +1 in the denominator prevents division-by-zero for stories with score = 0.
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular: flag stories that score above the dataset average.
# avg_score was computed with pandas .mean() above — equivalent to np.mean().
df["is_popular"] = df["score"] > avg_score

# ── 4. Save the Result ────────────────────────────────────────────────────────

os.makedirs("data", exist_ok=True)
output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)
print(f"\nSaved to {output_path}")
