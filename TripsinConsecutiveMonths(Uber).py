# Find the IDs of the drivers who completed at least one trip a month for at least two months in a row.

# Input DataFrame - uber_trips
                                                                   
import pandas as pd

df = uber_trips.copy()

df = df[df['is_completed'] == True]
df['year_month'] = df['trip_date'].dt.to_period('M')
# one record per driver per month
df = df[['driver_id','year_month']].drop_duplicates()

df = df.sort_values(['driver_id','year_month'])
df['diff'] = (
    df['year_month']
      .astype('int64')
      .groupby(df['driver_id'])
      .diff()
)

df['group'] = (df['diff']!=1).groupby(df['driver_id']).cumsum()
df['consecutive'] = (
    df.groupby(['driver_id', 'group'])
      .cumcount() + 1
)

df[df['consecutive']>=2]['driver_id'].unique()
