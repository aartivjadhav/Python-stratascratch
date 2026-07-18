# You have been asked to investigate whether there is a correlation between the average total order value and 
# the average time in minutes between placing an order and having it delivered per restaurant.
# You have also been told that the column order_total represents the gross order total for each order. 
# Therefore, you'll need to calculate the net order total. This is done by adding the tip_amount and subtracting both the discount_amount and refunded_amount from the order_total.
# Make sure correlation is rounded to 2 decimals.

# Input DataFrame - delivery_details

import pandas as pd

df = delivery_details[['restaurant_id','customer_placed_order_datetime','delivered_to_consumer_datetime']].copy()
df['net_total'] = delivery_details['order_total'] + delivery_details['tip_amount'] - delivery_details['discount_amount'] - delivery_details['refunded_amount']

df['minutes'] = (df['delivered_to_consumer_datetime'] - df['customer_placed_order_datetime']).dt.total_seconds()/60

df = df.groupby('restaurant_id').agg({
                                'minutes':'mean',
                                'net_total':'mean'
                            }).reset_index()

cor = round(df['minutes'].corr(df['net_total']),2)
result = pd.DataFrame({'correlation':[cor]}) 
result
