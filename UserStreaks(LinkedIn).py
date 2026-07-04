# Provided a table with user ID and the dates they visited the platform, 
# find the top 3 users with the longest continuous streak of visiting the platform up to August 10, 2022. 
# Output the user ID and the length of the streak.

# In case of a tie, display all users with the top three longest streak lengths.

# Input DataFrame - user_streaks

import pandas as pd

df = (
    user_streaks
    .drop_duplicates(['user_id', 'date_visited'])
    .sort_values(['user_id', 'date_visited'])
)

# Include records till August 10
df = df[df['date_visited'] <= '2022-08-10']

df['diff'] = df.groupby('user_id')['date_visited'].diff().dt.days

df['is_break'] = (df['diff'] != 1).astype(int)

df['streak_id'] = df.groupby('user_id')['is_break'].cumsum()

streaks = (
    df.groupby(['user_id', 'streak_id'])
      .size()
      .reset_index(name='streak_length')
)

result = (
    streaks.groupby('user_id')['streak_length']
           .max()
           .reset_index()
)

result['rank'] = result['streak_length'].rank(method='dense', ascending=False)

result = result[result['rank'] <= 3][['user_id', 'streak_length']]
