# You have the marketing_campaign table, which records in-app purchases by users. 
# Users making their first in-app purchase enter a marketing campaign, where they see call-to-actions for more purchases. 
# Find how many users made additional purchases due to the campaign's success.

# The campaign starts one day after the first purchase. 
# Users with only one or multiple purchases on the first day do not count, nor do users who later buy only 
# the same products from their first day.

# Input DataFrame - marketing_campaign
# Expected Output Type - pandas.DataFrame

import pandas as pd

df = marketing_campaign.copy()

# Step 1: First purchase date per user
first_purchase = df.groupby('user_id')['created_at'].min().reset_index()
first_purchase.columns = ['user_id', 'first_date']

df = df.merge(first_purchase, on='user_id')

# Step 2: Identify first-day products
first_day_products = df[df['created_at'] == df['first_date']][['user_id', 'product_id']].drop_duplicates()

# Step 3: Campaign window (after day 1)
campaign_purchases = df[df['created_at'] >= df['first_date'] + pd.Timedelta(days=1)]

# Step 4: Remove products already bought on first day
campaign_purchases = campaign_purchases.merge(
    first_day_products,
    on=['user_id', 'product_id'],
    how='left',
    indicator=True
)

campaign_purchases = campaign_purchases[campaign_purchases['_merge'] == 'left_only']

# Step 5: Count users with valid campaign-driven purchases
result = pd.DataFrame({
    'number_of_users': [campaign_purchases['user_id'].nunique()]
})

result
