# You're given a dataset of searches for properties on Airbnb. For simplicity, each row represents a unique host.
# Your task is to find the city whose hosts collectively list the greatest total number of amenities across all their properties.
# Treat amenities as a comma-separated list and count each listed entry as-is, even if the same amenities appear multiple times within the same property's amenities, 
# count each occurrence (do not deduplicate).
# If multiple cities tie for the highest total, return return all of those cities. Output the name of the city/cities.

# Input DataFrame - airbnb_search_details


# Import your libraries
import pandas as pd

# filter the required columns
df = airbnb_search_details[['city','id','amenities']]

# split the amenities list and count the amenities
df['amenities_count'] = df['amenities'].str.split(',').str.len()
df1 = df.groupby('city')['amenities_count'].sum().reset_index()

# rank to get the city with top amenities
result = df1[df1['amenities_count'].rank(method='dense',ascending=False) == 1]['city']

result = pd.DataFrame(result)
