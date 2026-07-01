# Find the 3-month rolling average of total revenue from purchases given a table with users, their purchase amount and date purchased. 
# Do not include returns which are represented by negative purchase values. 
# Output the year-month (YYYY-MM) and 3-month rolling average of revenue, sorted from earliest month to latest month.

# A 3-month rolling average is defined by calculating the average total revenue from all user purchases for the current month 
# and previous two months. The first two months will not be a true 3-month rolling average since we are not given data from last year.
# Assume each month has at least one purchase.

# Input DataFrame - amazon_purchases
# Expected Output Type - pandas.DataFrame

import pandas as pd

df = amazon_purchases.copy()

# Step 1: Remove returns
df = df[df['purchase_amt'] > 0]

# Step 2: Create year-month
df['year_month'] = df['created_at'].dt.to_period('M')

# Step 3: Monthly revenue
monthly_revenue = df.groupby('year_month')['purchase_amt'].sum().reset_index()

# Ensure correct order (for rolling)
monthly_revenue = monthly_revenue.sort_values('year_month')

# Step 4: 3-month rolling average
monthly_revenue['rolling_avg_3m'] = (
    monthly_revenue['purchase_amt']
    .rolling(window=3, min_periods=1)
    .mean()
    .round(2)
)

# Step 5: Final formatting
monthly_revenue['year_month'] = monthly_revenue['year_month'].astype(str)

result = monthly_revenue[['year_month', 'rolling_avg_3m']]

result
