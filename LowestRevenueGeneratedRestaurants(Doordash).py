# Write a query that returns a list of the bottom 2% revenue generating restaurants. Return a list of restaurant IDs and their total revenue from when customers placed orders in May 2020.
# You can calculate the total revenue by summing the order_total column. And you should calculate the bottom 2% by partitioning the total revenue into evenly distributed buckets.
# Input DataFrame - doordash_delivery

import pandas as pd

df = doordash_delivery[(doordash_delivery['customer_placed_order_datetime'].dt.month == 5)
        & (doordash_delivery['customer_placed_order_datetime'].dt.year == 2020)][['restaurant_id','customer_placed_order_datetime','order_total']]

df = df.groupby('restaurant_id')['order_total'].sum().reset_index().sort_values(by='order_total')
df['bucket'] = pd.qcut(df['order_total'],q=50,duplicates='drop', labels=False)

result = df[df['bucket'] == 0][['restaurant_id','order_total']]
