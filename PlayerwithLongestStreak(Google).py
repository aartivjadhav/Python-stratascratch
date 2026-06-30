# Player with Longest Streak

# You are given a table of tennis players and their matches that they could either win (W) or lose (L). 
# Find the longest streak of wins. A streak is a set of consecutive won matches of one player. 
# The streak ends once a player loses their next match.

# For this question, disregard edge cases such as: players who never lose, streaks that start before the first loss, and streaks that 
# continue after the final match.

# Input DataFrame - players_results
# Expected Output Type - pandas.DataFrame


import pandas as pd

df = players_results.sort_values(['player_id', 'match_date']).copy()

# Convert result to binary
df['win'] = (df['match_result'] == 'W').astype(int)

# Create reset groups (each loss breaks streak)
df['group'] = df.groupby('player_id')['win'].apply(
    lambda x: (x == 0).cumsum()
).reset_index(level=0, drop=True)

# Keep only wins
wins = df[df['win'] == 1]

# Count streak length per group
streaks = wins.groupby(['player_id', 'group']).size().reset_index(name='streak_len')

# Max streak per player
result = streaks.groupby('player_id')['streak_len'].max().reset_index()

result
