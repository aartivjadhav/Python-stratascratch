# Select the most popular client_id based on the number of users who individually have at least 50% of their events from the following list: 
# 'video call received', 'video call sent', 'voice call received', 'voice call sent'.

# Input DataFrame - fact_events

import pandas as pd

df = fact_events[fact_events['event_type'].isin(['video call received','video call sent','voice call received','voice call sent'])]

df = df.groupby(['client_id','user_id'])['event_type'].count().rename('event_count').reset_index()
total_events = fact_events.groupby(['client_id','user_id'])['event_type'].count().rename('total_count').reset_index()

merged = total_events.merge(df,on=['client_id','user_id'],how='left')

merged['is_50_or_more'] = (merged['event_count']/merged['total_count']>=0.5).astype(int)
merged['event_count'] = merged['event_count'].fillna(0)
merged = merged.groupby('client_id')['is_50_or_more'].sum().reset_index()
result = merged[merged['is_50_or_more'] == merged['is_50_or_more'].max()]
result
