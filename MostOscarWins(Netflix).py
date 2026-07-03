# Find the genre of the person with the most number of oscar winnings

# Find the genre of the person with the most number of oscar winnings.
# If there are more than one person with the same number of oscar wins, 
# return the first one in alphabetic order based on their name. Use the names as keys when joining the tables.

import pandas as pd

# Merge on names
df = oscar_nominees.merge(
    nominee_information,
    left_on='nominee',
    right_on='name'
)

# Keep only winners
df = df[df['winner'] == True]

# Count wins per person
win_counts = df.groupby('name').size().reset_index(name='wins')

# Get max wins
max_wins = win_counts['wins'].max()

# Filter people with max wins
top_people = win_counts[win_counts['wins'] == max_wins]

# Break ties alphabetically
top_person = top_people.sort_values('name').iloc[0]['name']

# Get genre of that person
result = nominee_information[nominee_information['name'] == top_person]['top_genre'].iloc[0]

