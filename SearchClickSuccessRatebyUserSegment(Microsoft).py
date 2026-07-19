# Calculate the search success rate for new users versus existing users. A successful search is one where the first click event occurs within 30 seconds of the search event.
# Group all users into two segments:
# •  new (registered within the last 30 days covered by the dataset — that is, on or after 30 days before the most recent date in the dataset)
# •  existing (registered earlier).
# Return one row per user segment with total searches, successful searches, and success rate.

# Input DataFrames - search_events, accounts
import pandas as pd
df = accounts.copy()
df['is_new'] = (accounts['registration_date']>=(accounts['registration_date'].max() - pd.Timedelta(days=30))).astype(int)

df_se = search_events.sort_values(by=['user_id','event_timestamp'])[['user_id','event_timestamp','event_type']]

df_se['previous_event'] = df_se.groupby('user_id')['event_type'].shift(1)
df_se

df_se['time_diff'] = (
    df_se['event_timestamp'].diff().dt.total_seconds()
    .where(
        (df_se['previous_event'] == 'search') &
        (df_se['event_type'] == 'click'),
        0
    )
)

df_merged = df_se.merge(df,on='user_id')[['user_id','event_timestamp','event_type','time_diff','is_new']]

result = df_merged.groupby('is_new').agg(\
        total_searches = ('event_type', lambda x: (x == 'search').sum()),
        successful_search=('time_diff',lambda x: ((x <=30) & (x > 0)).sum())
    ).reset_index()

result = result.rename(columns={'is_new':'segments'})
result['segments'] = result['segments'].map({
    0: 'existing',
    1: 'new'
})
result['success_rate'] = (result['successful_search']*100/result['total_searches']).round(2)
result
