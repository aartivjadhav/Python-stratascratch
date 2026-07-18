# Calculate the share of new and existing users for each month in the table. Output the month, share of new users, and share of existing users as a ratio.
# New users are defined as users who started using services in the current month (there is no usage history in previous months). 
# Existing users are users who used services in the current month, and who also used services in any prior month of 2020.
# Assume that the dates are all from the year 2020 and that users are contained in user_id column.

# Input DataFrame - fact_events

df = fact_events.copy()
df['month'] = df['time_id'].dt.month
df['min_month'] = df.groupby('user_id')['month'].transform(min)
df = df.drop_duplicates(subset=['user_id','month'])
df['is_new'] = (df['month'] <= df['min_month']).astype(int)

df1 = df.pivot_table(index='month',columns='is_new',aggfunc='size', fill_value=0)
df1.columns = ['existing_users', 'new_users']
df1['total'] = df1['existing_users'] + df1['new_users']
df1['existing_users'] = df1['existing_users']/df1['total']
df1['new_users'] = df1['new_users']/df1['total']
result = df1.reset_index()
