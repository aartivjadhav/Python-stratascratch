
# Compare the total number of comments made by users in each country during December 2019 and January 2020.
# For each month, rank countries by their total number of comments in descending order.
# Countries with the same total should share the same rank, and the next rank should increase by one (without skipping numbers).
# Return the names of the countries whose rank improved from December to January (that is, their rank number became smaller).

# Input DataFrames - 
# fb_comments_count
# fb_active_users

import pandas as pd

# Filter comments made during December 2019 and January 2020
comments = fb_comments_count[
    (fb_comments_count["created_at"].dt.date >= pd.to_datetime("2019-12-01").date())
    & (fb_comments_count["created_at"].dt.date <= pd.to_datetime("2020-01-31").date())
]

# Merge comments with user information to retrieve each user's country
comments = fb_active_users.merge(comments, on="user_id")

# Extract the month name from the comment date
comments["month"] = comments["created_at"].dt.month_name()

# Calculate the total number of comments made by each country for each month
country_comments = (
    comments.groupby(["country", "month"])["number_of_comments"]
    .sum()
    .unstack()
    .reset_index()
    .fillna(0)
)

# Rank countries within each month based on total comments
country_comments["dec_rank"] = country_comments["December"].rank(
    method="dense",
    ascending=False,
)

country_comments["jan_rank"] = country_comments["January"].rank(
    method="dense",
    ascending=False,
)

# Return countries whose rank improved in January compared to December
result = country_comments.loc[
    country_comments["jan_rank"] < country_comments["dec_rank"],
    ["country"],
]
