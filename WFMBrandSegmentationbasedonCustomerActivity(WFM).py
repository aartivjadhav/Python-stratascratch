# WFM would like to segment the customers in each of their store brands into Low, Medium, and High segmentation. 
# The segments are to be based on a customer's average basket size which is defined as (total sales / count of transactions), per customer.
# The segment thresholds are as follows:
# If average basket size is more than $30, then Segment is “High”.
# If average basket size is between $20 and $30, then Segment is “Medium”.
# If average basket size is less than $20, then Segment is “Low”.
# Summarize the number of unique customers, the total number of transactions, total sales, and average basket size, grouped by store brand and segment for 2017.
# Your output should include the brand, segment, number of customers, total transactions, total sales, and average basket size.

# Input DataFrames - wfm_transactions, wfm_stores
                                                                                                                                                    
import pandas as pd
import numpy as np

df = wfm_transactions[wfm_transactions['transaction_date'].dt.year == 2017]
df = df.merge(wfm_stores,on='store_id')

df = df.groupby(['store_brand','customer_id']).agg({
                                            'transaction_id':'nunique',
                                            'sales':'sum'
                                        }).reset_index()
df = df.rename(columns = {'transaction_id':'total_transactions','sales':'total_sales'})               

df['avg_basket_size'] = (df['total_sales']/df['total_transactions'])
bins = [0,20,30,np.inf]
labels = ['Low','Medium','High']
df['segments'] = pd.cut(df['avg_basket_size'],bins=bins,labels=labels)

df = df.groupby(['store_brand','segments'],observed=True).agg(
                            {
                                'customer_id':'count',
                                'total_transactions':'sum',
                                'total_sales':'sum'
                            }
                        ).reset_index()

df['average_basket_size'] = (df['total_sales']/df['total_transactions'])
df
