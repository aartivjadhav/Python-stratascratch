# You work as a data analyst for an e-commerce platform. The sales team needs to understand the net revenue performance of Product ID 'PROD-2891' in the US market 
# for purchases made during a recent two-week period. The dataset contains purchases and refunds. Refunds link to their original purchase via the original_transaction_id field.
# Calculate daily net revenue for April 15-28, 2025. Include completed purchases of PROD-2891 made in the US during that period, and 
# any completed refunds linked to those purchases, regardless of when the refund was processed or which country is recorded on the refund row. Show zero for days with no activity. 
# Return transaction_date and daily_net_revenue.

# Input DataFrame - product_sales

# Import libraries
import pandas as pd

# Purchases
purchases = product_sales[
    (product_sales['type'] == 'purchase') &
    (product_sales['product_id'] == 'PROD-2891') &
    (product_sales['country'] == 'US') &
    (product_sales['status'] == 'completed') &
    (product_sales['transaction_date'].between('2025-04-15', '2025-04-28'))
]

# Refunds linked to those purchases
refunds = product_sales[
    (product_sales['type'] == 'refund') &
    (product_sales['status'] == 'completed') &
    (product_sales['original_transaction_id'].isin(purchases['transaction_id']))
]

# Combine
df = pd.concat([
    purchases[['transaction_date', 'amount']],
    refunds[['transaction_date', 'amount']]
])

daily_sales = df.groupby('transaction_date')['amount'].sum()
daily_sales = daily_sales.asfreq('D', fill_value=0)

date_range = pd.date_range('2025-04-15', '2025-04-28')

result = (
    daily_sales
    .reindex(date_range, fill_value=0)
    .rename_axis('transaction_date')
    .reset_index(name='daily_net_revenue')
)
