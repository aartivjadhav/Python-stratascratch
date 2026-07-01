# Actor Rating Difference Analysis -
# You are given a dataset of actors and the films they have been involved in, including each film's release date and rating. 
# For each actor, calculate the difference between the rating of their most recent film and their average rating across 
# all previous films (the average rating excludes the most recent one).

# Return a list of actors along with their average lifetime rating, the rating of their most recent film, 
# and the difference between the two ratings. Round the difference calculation to 2 decimal places. 
# If an actor has only one film, return 0 for the difference and their only film’s rating for both the average and latest rating fields.

# Input DataFrame - actor_rating_shift

import pandas as pd

ratings = actor_rating_shift.copy()

# Identify each actor's most recent film
is_recent = (
    ratings.groupby('actor_name')['release_date']
    .transform('max')
    .eq(ratings['release_date'])
)

# Average rating excluding the latest film
avg_ratings = (
    ratings.loc[~is_recent]
    .groupby('actor_name')['film_rating']
    .mean()
    .rename('avg_rating')
    .reset_index()
)

# Latest film information
latest = (
    ratings.loc[is_recent, ['actor_name', 'film_rating']]
    .rename(columns={'film_rating': 'latest_rating'})
)

# Combine results
result = latest.merge(avg_ratings, on='actor_name', how='left')

# Handle actors with only one film
result['avg_rating'] = result['avg_rating'].fillna(result['latest_rating'])

# Difference
result['rating_diff'] = (
    result['latest_rating'] - result['avg_rating']
).round(2)

result = result[
    ['actor_name', 'avg_rating', 'latest_rating', 'rating_diff']
]


