# For the video (or videos) that received the most user flags, how many of these flags were reviewed by YouTube? Output the video ID and the corresponding number of reviewed flags.  
# Ignore flags that do not have a corresponding flag_id.

# Input DataFrames - user_flags, flag_review

import pandas as pd

# drop records where no flag_id present
uf = user_flags.dropna(subset=['flag_id'])

# find video ids with maximum of user flags
df = uf.groupby('video_id')['flag_id'].nunique().reset_index(name='flag_count')
df = df[df['flag_count']==df['flag_count'].max()]
df = df.merge(uf,on='video_id')[['flag_id','video_id']]

# join with flag_review and get number oof reviewed flags
df = df.merge(flag_review,on='flag_id')
df = df[df['reviewed_by_yt']==True]
df = df.groupby('video_id')['flag_id'].nunique().reset_index(name='num_reviewed_flags')
