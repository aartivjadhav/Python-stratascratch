# Find the most profitable location. Write a query that calculates the average signup duration in days and the average transaction amount for each location. 
# Then, calculate the ratio of average transaction amount to average duration.
# Your output should include the location, average signup duration (in days), average transaction amount, and the ratio. Sort the results by ratio in descending order.

# Input DataFrames - signups, transactions

import pandas as pd

signups['duration'] = (signups['signup_stop_date'] - signups['signup_start_date']).dt.days

result = signups.groupby('location')['duration'].mean().reset_index()

merged = signups.merge(transactions,on = 'signup_id')

df = merged.groupby('location')['amt'].mean().reset_index()

result = result.merge(df,on='location')
result['ratio'] = result['amt']/result['duration']

result = result.sort_values(by='ratio', ascending=False)
result
