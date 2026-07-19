# Given users' session logs, calculate how many hours each user was active in total across all recorded sessions.
# Note: The session starts when state=1 and ends when state=0.

# Input DataFrame - cust_tracking

# Import your libraries
import pandas as pd

# Start writing code
# sort the records to get the time difference
df = cust_tracking.sort_values(by=['cust_id','timestamp']).copy()

# get the previous state
df['previous_state'] = df.groupby('cust_id')['state'].shift()

# calculate time difference
df['time'] = df.groupby('cust_id')['timestamp'].diff()/3600

# filter the rows to get the session end rows
df = df[(df['previous_state']==1) & (df['state']==0)]

# find the total active time
result = df.groupby('cust_id')['time'].sum().reset_index(name='session_time')
result
