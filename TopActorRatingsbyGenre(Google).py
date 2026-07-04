# Find the top actors based on their average movie rating within the genre they appear in most frequently.
# •  For each actor, determine their most frequent genre (i.e., the one they’ve appeared in the most).
# •   If there is a tie in genre count, select the genre where the actor has the highest average rating.
# •   If there is still a tie in both count and rating, include all tied genres for that actor.


# Rank all resulting actor + genre pairs in descending order by their average movie rating.
# •  Return all pairs that fall within the top 3 ranks (not simply the top 3 rows), including ties.
# •  Do not skip rank numbers — for example, if two actors are tied at rank 1, the next rank is 2 (not 3).

# input DataFrame - top_actors_rating


import pandas as pd

# Count appearances and average rating for each actor-genre pair
df = (
    top_actors_rating
    .groupby(['actor_name', 'genre'])
    .agg(
        genre_cnt=('genre', 'size'),
        avg_rating=('movie_rating', 'mean')
    )
    .reset_index()
)

# Step 1: Keep genres with the maximum count for each actor
max_cnt = df.groupby('actor_name')['genre_cnt'].transform('max')
df = df[df['genre_cnt'] == max_cnt]

# Step 2: Among those, keep genres with the highest average rating
max_rating = df.groupby('actor_name')['avg_rating'].transform('max')
df = df[df['avg_rating'] == max_rating]

# If there are ties in both count and rating, all rows are retained

# Step 3: Rank globally by average rating
df['rank'] = df['avg_rating'].rank(method='dense', ascending=False)

# Step 4: Return top 3 ranks (including ties)
result = (
    df[df['rank'] <= 3]
    .sort_values(['rank', 'actor_name', 'genre'])
    [['actor_name', 'genre', 'avg_rating']]
)
