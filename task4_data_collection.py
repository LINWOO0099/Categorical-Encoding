"""
TrendPulse — Task 4: Visualizations
Loads trends_analysed.csv from Task 3 and produces 3 charts
plus a combined dashboard, all saved as PNGs in outputs/.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ── 1. Setup ──────────────────────────────────────────────────────────────────

df = pd.read_csv("data/trends_analysed.csv")

# is_popular was saved as a boolean string — coerce it back just in case
df["is_popular"] = df["is_popular"].astype(bool)

os.makedirs("outputs", exist_ok=True)

# Colour palette used consistently across charts
CAT_COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"]

# ── 2. Chart 1: Top 10 Stories by Score ──────────────────────────────────────

# Sort descending and take the top 10
top10 = df.nlargest(10, "score").copy()

# Truncate long titles so the y-axis stays readable
top10["short_title"] = top10["title"].apply(
    lambda t: t[:50] + "…" if len(t) > 50 else t
)

fig1, ax1 = plt.subplots(figsize=(10, 6))

# horizontal bar — longer bars = higher score, easy to scan
ax1.barh(top10["short_title"], top10["score"], color="#4C72B0", edgecolor="white")

# Invert y-axis so the highest-scoring story appears at the top
ax1.invert_yaxis()

ax1.set_title("Top 10 Stories by Score", fontsize=14, fontweight="bold", pad=12)
ax1.set_xlabel("Score (upvotes)")
ax1.set_ylabel("Story Title")
ax1.tick_params(axis="y", labelsize=8)

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png", dpi=150)
plt.close(fig1)                        # close so it doesn't bleed into next chart
print("Saved: outputs/chart1_top_stories.png")

# ── 3. Chart 2: Stories per Category ─────────────────────────────────────────

# Count stories per category, sorted descending for visual clarity
cat_counts = df["category"].value_counts().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(8, 5))

bars = ax2.bar(
    cat_counts.index,
    cat_counts.values,
    color=CAT_COLORS[: len(cat_counts)],  # one colour per bar
    edgecolor="white",
    width=0.6,
)

# Annotate each bar with its count so exact numbers are visible
for bar in bars:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        str(int(bar.get_height())),
        ha="center",
        va="bottom",
        fontsize=9,
    )

ax2.set_title("Stories per Category", fontsize=14, fontweight="bold", pad=12)
ax2.set_xlabel("Category")
ax2.set_ylabel("Number of Stories")
ax2.set_ylim(0, cat_counts.max() + 3)   # headroom above tallest bar

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png", dpi=150)
plt.close(fig2)
print("Saved: outputs/chart2_categories.png")

# ── 4. Chart 3: Score vs Comments (scatter) ───────────────────────────────────

# Split into popular and non-popular groups for separate plotting
popular     = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

fig3, ax3 = plt.subplots(figsize=(8, 6))

ax3.scatter(
    not_popular["score"], not_popular["num_comments"],
    color="#4C72B0", alpha=0.6, s=50, label="Not Popular"
)
ax3.scatter(
    popular["score"], popular["num_comments"],
    color="#DD8452", alpha=0.8, s=70, marker="D", label="Popular (above avg score)"
)

ax3.set_title("Score vs Number of Comments", fontsize=14, fontweight="bold", pad=12)
ax3.set_xlabel("Score (upvotes)")
ax3.set_ylabel("Number of Comments")
ax3.legend(fontsize=9)

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png", dpi=150)
plt.close(fig3)
print("Saved: outputs/chart3_scatter.png")

# ── Bonus: Dashboard — all 3 charts in one figure ────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(22, 7))
fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold", y=1.01)

# -- Panel 1: Top 10 horizontal bar --
axes[0].barh(top10["short_title"], top10["score"], color="#4C72B0", edgecolor="white")
axes[0].invert_yaxis()
axes[0].set_title("Top 10 Stories by Score", fontsize=11, fontweight="bold")
axes[0].set_xlabel("Score")
axes[0].tick_params(axis="y", labelsize=7)

# -- Panel 2: Stories per category --
axes[1].bar(
    cat_counts.index,
    cat_counts.values,
    color=CAT_COLORS[: len(cat_counts)],
    edgecolor="white",
    width=0.6,
)
for bar in axes[1].patches:
    axes[1].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.2,
        str(int(bar.get_height())),
        ha="center", va="bottom", fontsize=8,
    )
axes[1].set_title("Stories per Category", fontsize=11, fontweight="bold")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")
axes[1].set_ylim(0, cat_counts.max() + 3)

# -- Panel 3: Scatter --
axes[2].scatter(
    not_popular["score"], not_popular["num_comments"],
    color="#4C72B0", alpha=0.6, s=40, label="Not Popular"
)
axes[2].scatter(
    popular["score"], popular["num_comments"],
    color="#DD8452", alpha=0.8, s=60, marker="D", label="Popular"
)
axes[2].set_title("Score vs Comments", fontsize=11, fontweight="bold")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend(fontsize=8)

plt.tight_layout()
plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("Saved: outputs/dashboard.png")

print("\nAll charts saved to outputs/")
