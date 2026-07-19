# Identify all products that experienced a turnaround in user engagement: at least 3 consecutive months of declining monthly active users followed by at least 3 consecutive months of growth.
# For each product that matches this pattern, return the product name, the month when the decline started, the month when growth resumed, 
# and the growth ratio from the lowest point to the most recent peak, calculated as: (peak_users - lowest_users) / lowest_users.

# Input DataFrame - product_engagement

import pandas as pd
df = product_engagement.copy()

df = df.groupby(['product_name','month_start'])['monthly_active_users'].sum().reset_index()
df = df.sort_values(by=['product_name','month_start'])
df['change'] = df.groupby('product_name')['monthly_active_users'].diff()
df['trend'] = df['change'].map(lambda x:'D' if x<0 else 'G' if x>0 else 'S')
df['grp'] = (df['trend'] != df.groupby('product_name')['trend'].shift()).cumsum()
runs = (
    df.groupby(['product_name','grp','trend'])
      .agg(
          length=('trend','size'),
          start_month=('month_start','min'),
          end_month=('month_start','max')
      )
      .reset_index()
)

runs['next_trend'] = runs.groupby('product_name')['trend'].shift(-1)
runs['next_length'] = runs.groupby('product_name')['length'].shift(-1)

matches = runs[
    (runs['trend']=='D') &
    (runs['length']>=3) &
    (runs['next_trend']=='G') &
    (runs['next_length']>=3)
]

results = []

for _, row in matches.iterrows():

    product = row['product_name']
    
    decline_start = row['start_month']
    
    growth_start = (
        runs[
            (runs.product_name == product) &
            (runs.grp == row.grp + 1)
        ]['start_month']
        .iloc[0]
    )

    temp = df[
        (df.product_name == product) &
        (df.month_start >= decline_start)
    ]

    lowest_users = temp['monthly_active_users'].min()

    peak_users = temp[
        temp.month_start >= growth_start
    ]['monthly_active_users'].max()

    growth_ratio = (
        (peak_users - lowest_users) /
        lowest_users
    )

    results.append({
        'product_name': product,
        'decline_started': decline_start,
        'growth_resumed': growth_start,
        'growth_ratio': growth_ratio
    })

result = pd.DataFrame(results)
