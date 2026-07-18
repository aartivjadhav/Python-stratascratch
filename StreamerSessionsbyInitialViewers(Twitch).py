# Return the number of streamer sessions for each user whose very first session was as a viewer.
# Include the user ID and count of streamer sessions for users whose earliest session (by session_start) was a 'viewer' session, regardless of whether they ever had a streamer session later. 
# Sort the results by streamer session count in descending order, then by user ID in ascending order.

# Input DataFrame - twitch_sessions

import pandas as pd

df = twitch_sessions.groupby('user_id')['session_start'].min().reset_index()

df = df.merge(twitch_sessions,on=['user_id','session_start'])

df = df[df['session_type'] == 'viewer'][['user_id']].merge(twitch_sessions,on='user_id')

df['is_streamer'] = df['session_type'] == 'streamer'

df = df.groupby('user_id')['is_streamer'].sum().reset_index(name='streamer_session_count')

df = df.sort_values(['streamer_session_count','user_id'],ascending=[False,True])
