# You are given a dataset that tracks user activity. The dataset includes information about the date of user activity, the account_id associated with the activity, 
# and the user_id of the user performing the activity. Each row in the dataset represents a user’s activity on a specific date for a particular account_id.
# Your task is to calculate the monthly retention rate for users for each account_id for December 2020 and January 2021. 
# The retention rate is defined as the percentage of users active in a given month who have activity in any future month.
# For instance, a user is considered retained for December 2020 if they have activity in December 2020 and any subsequent month (e.g., January 2021 or later). 
# Similarly, a user is retained for January 2021 if they have activity in January 2021 and any later month (e.g., February 2021 or later).
# The final output should include the account_id and the ratio of the retention rate in January 2021 to the retention rate in December 2020 for each account_id. 
# If there are no users retained in December 2020, the retention rate ratio should be set to 0.

# Input DataFrame - sf_events
import pandas as pd

df = sf_events.copy()

df['month_year'] = df['record_date'].dt.to_period('M').astype(str)
df = df.sort_values(by='month_year')

df1 = df.groupby(['account_id','month_year','user_id'],observed=False)['user_id'].nunique().unstack().reset_index().fillna(0)

df1 = df1.set_index(['account_id','month_year'])

accnts = df1.index.get_level_values(0).unique()

result = []
for a in accnts:
    row = df1.loc[a,'2020-12'] if '2020-12' in df1.loc[a].index else pd.Series()
    dec_users = set(row[row==1].index)
        
    row = df1.loc[a,'2021-01'] if '2021-01' in df1.loc[a].index else pd.Series()
    jan_users = set(row[row==1].index)
        
    row = df1.loc[a,'2021-02'] if '2021-02' in df1.loc[a].index else pd.Series()
    feb_users = set(row[row==1].index) if not row.empty else set()
        
    dec_jan_feb_users = dec_users.intersection(jan_users,feb_users)
        
    dec_retention_rate = round(len(dec_jan_feb_users)/len(dec_users),2)

    jan_feb_users = jan_users.intersection(feb_users)
    jan_retention_rate = round(len(jan_feb_users)/len(jan_users),2)

    result.append({'account_id':a,'dec_retention_rate':dec_retention_rate,'jan_retention_rate':jan_retention_rate})

result = pd.DataFrame(result)
result['retention_ratio'] = result['jan_retention_rate']/result['dec_retention_rate']
result = result.fillna(0)
