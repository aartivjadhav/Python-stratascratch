# You are managing a task scheduling system where each task has a specific start and end time. 
# Multiple tasks can run simultaneously if there are enough CPUs available, but each CPU can only run one task at a time.
# Given a list of task execution intervals, determine the minimum number of CPUs required to execute all tasks without any conflicts. 
# When processing the data, duplicate task entries should only be counted once, and tasks with missing start or end times should be excluded from the calculation.
# Tasks without names can still be included as long as they have valid execution times. 
# Note that when a task ends at the exact moment another task starts, they do not conflict since the CPU can be reused immediately.
# Return the minimum number of CPUs required.

# Input DataFrame - task_schedule

import pandas as pd

# Start writing code
df = task_schedule.sort_values(by='task_id').copy()

df.drop_duplicates(subset=['start_time','end_time'],inplace=True,keep='first')
df.dropna(subset=['start_time','end_time'],inplace=True,axis=0)
    
df['task_name'].fillna('Task_'+df['task_id'].astype(str),inplace=True)

# combine start_time and end_time using melt, assign 1 to start_time -1 to end_time, sort them and cumsum
df_long = pd.melt(df,
                id_vars = ['task_id','task_name'],
                value_vars = ['start_time','end_time'],
                value_name = 'time',
                var_name = 'time_type',
                )

df_long['flag'] = df_long['time_type'].map({
    'start_time': 1,
    'end_time': -1
})

df_long = df_long.sort_values(['time','flag'])

num_cpus = df_long['flag'].cumsum().max()
