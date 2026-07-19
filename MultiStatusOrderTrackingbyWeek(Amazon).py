# Amazon tracks orders through multiple stages from placement to delivery. 
# Each order has three key dates: when it was ordered, when it was shipped, and when it was received by the customer.
# Create a weekly report showing how many orders are in their latest new status for that week, with weeks starting on Monday. 
# An order should be counted from its order week through its delivery week only. 
# Before shipment it counts as pending; after shipment and before delivery it counts as shipped; in the week it is received it counts as delivered. 
# Do not continue counting delivered orders in subsequent weeks.
# Output the week_start_date, count of pending_orders, count of shipped_orders, and count of delivered_orders.

# Input DataFrame - shipment_tracking

import pandas as pd
import numpy as np

# 1. Copy and convert columns to datetime
df = shipment_tracking.copy()
df['ordered_date'] = pd.to_datetime(df['ordered_date'])
df['shipped_date'] = pd.to_datetime(df['shipped_date'])
df['delivered_date'] = pd.to_datetime(df['delivered_date'])

# 2. Determine the latest overall date in the dataset to act as the report cutoff for open orders
report_end_date = max(
    df['ordered_date'].max(), 
    df['shipped_date'].max(), 
    df['delivered_date'].max()
)

# 3. Get Monday start dates (W-SUN period start gives Monday)
df['order_week'] = df['ordered_date'].dt.to_period('W-SUN').dt.start_time
df['ship_week'] = df['shipped_date'].dt.to_period('W-SUN').dt.start_time

# If delivered_date is missing, project its tracking window up to the report's end date
df['delivery_week'] = (
    df['delivered_date']
    .fillna(report_end_date)
    .dt.to_period('W-SUN')
    .dt.start_time
)

# 4. Generate the range of active weeks and explode
df['week_start'] = df.apply(
    lambda x: pd.date_range(x['order_week'], x['delivery_week'], freq='W-MON'),
    axis=1
)

df_exploded = df.explode('week_start')

# 5. Determine the status with strict null checking
def determine_status(row):
    # It only counts as delivered if it actually HAS a delivery date and matches the week
    if pd.notna(row['delivered_date']) and row['week_start'] == row['delivery_week']:
        return 'delivered_orders'
    # It counts as shipped if it HAS a ship date and we are past or at that week
    elif pd.notna(row['ship_week']) and row['week_start'] >= row['ship_week']:
        return 'shipped_orders'
    # Otherwise, it's pending (either not shipped yet, or shipped but never delivered)
    else:
        return 'pending_orders'

df_exploded['status'] = df_exploded.apply(determine_status, axis=1)

# 6. Pivot and clean final output
report = (
    df_exploded.groupby(['week_start', 'status'])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

# Ensure all status columns exist even if a specific week has 0 count
for col in ['pending_orders', 'shipped_orders', 'delivered_orders']:
    if col not in report.columns:
        report[col] = 0

report = report.rename(columns={'week_start': 'week_start_date'})
report = report[['week_start_date', 'pending_orders', 'shipped_orders', 'delivered_orders']]
