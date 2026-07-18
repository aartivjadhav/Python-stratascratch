# Write a query that returns every employee that has ever worked for the company. 
# For each employee, calculate the greatest number of employees that worked for the company during their tenure and the first date that number was reached. 
# The termination date of an employee should not be counted as a working day.
# Your output should have the employee ID, greatest number of employees that worked for the company during the employee's tenure, and first date that number was reached.

# Input DataFrame - uber_employees

import pandas as pd
uber_employees.sort_values(by='hire_date')
uber_employees['termination_date'] = uber_employees['termination_date'].fillna(pd.Timestamp.now().normalize())

df = pd.DataFrame({
    'dates': uber_employees['hire_date'],
    'emp_count': 1
})

df1 = pd.DataFrame({
    'dates': uber_employees['termination_date'],
    'emp_count': -1
})
df1 = df1.dropna()

emp_nums = pd.concat([df,df1])
emp_nums = emp_nums.groupby('dates')['emp_count'].sum().reset_index()
emp_nums = emp_nums.sort_values('dates').reset_index(drop=True)
emp_nums['running_total'] = emp_nums['emp_count'].cumsum()

def get_max_emp(row):
    hire_date = row['hire_date']
    termination_date = row['termination_date']
    
    temp_df = emp_nums[(emp_nums['dates']>=hire_date) & (emp_nums['dates']<termination_date)]
    temp_max = temp_df['running_total'].max() if not temp_df.empty else 0
    temp_date = temp_df[temp_df['running_total'] == temp_max]['dates'].min()
    return pd.Series([temp_date,temp_max]) 

uber_employees[['first_date','max_emps']] = uber_employees.apply(get_max_emp,axis=1)

result = uber_employees[['id','max_emps','first_date']]

result
