# Given a table of purchases by date, calculate the month-over-month percentage change in revenue. 
# The output should include the year-month date (YYYY-MM) and percentage change, rounded to the 2nd decimal point, and sorted 
# from the beginning of the year to the end of the year.
# The percentage change column will be populated from the 2nd month forward and can be calculated as 
#   ((this month's revenue - last month's revenue) / last month's revenue)*100.
# input DataFrame - sf_transactions

import pandas as pd

df = sf_transactions.copy()

# Step 1: convert to month
df['year_month'] = df['created_at'].dt.to_period('M')

# Step 2: aggregate revenue per month
df = df.groupby('year_month', as_index=False)['value'].sum()

# Step 3: sort chronologically
df = df.sort_values('year_month')

# Step 4: month-over-month % change
df['percent_change'] = (df['value'].pct_change() * 100).round(2)

# Step 5: format output
df['year_month'] = df['year_month'].astype(str)

df
