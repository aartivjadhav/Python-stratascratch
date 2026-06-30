# You are given the list of Facebook friends and the list of Facebook pages that users follow. 
# Your task is to create a new recommendation system for Facebook. For each Facebook user, 
# find pages that this user doesn't follow but at least one of their friends does. 
# Output the user ID and the ID of the page that should be recommended to this user.

# DataFrames - users_friends, users_pages
# Expected Output Type - pandas.DataFrame

import pandas as pd

# Step 1: Friends → Pages mapping
friend_pages = users_friends.merge(
    users_pages,
    left_on='friend_id',
    right_on='user_id',
    how='inner'
)[['user_id_x', 'page_id']]

friend_pages = friend_pages.rename(columns={'user_id_x': 'user_id'})

# Step 2: Remove pages already followed by the user
recommendations = friend_pages.merge(
    users_pages,
    on=['user_id', 'page_id'],
    how='left',
    indicator=True
)
recommendations = recommendations[recommendations['_merge'] == 'left_only']

# Step 3: Final output
result = recommendations[['user_id', 'page_id']].drop_duplicates().reset_index(drop=True)

result
