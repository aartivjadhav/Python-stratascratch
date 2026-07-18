# Write a query to find the number of days between the longest and least tenured employee still working for the company. 
# Your output should include the number of employees with the longest-tenure, the number of employees with the least-tenure, 
# and the number of days between both the longest-tenured and least-tenured hiring dates.

# Input DataFrame - uber_employees

# Import your libraries
import pandas as pd

df = uber_employees[uber_employees['termination_date'].isna()]

df['num_of_days'] = (pd.to_datetime('today') - df['hire_date']).dt.days

df1 = df[(df['num_of_days'] == df['num_of_days'].min()) | (df['num_of_days'] == df['num_of_days'].max())]

df1 = df1.groupby('hire_date')['id'].count().reset_index().sort_values(by='hire_date')

least_tenure_row = df1.loc[df1['hire_date'].idxmax()]
max_tenure_row = df1.loc[df1['hire_date'].idxmin()]

result = pd.DataFrame({'longest-tenure-emps':max_tenure_row['id'] ,
                        'least-tenure-emps':least_tenure_row['id'] ,
                        'num-of-days': [(least_tenure_row['hire_date']-max_tenure_row['hire_date']).days]
})

result
