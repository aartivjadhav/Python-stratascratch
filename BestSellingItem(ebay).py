# Find the best-selling item for each month (no need to separate months by year). 
# The best-selling item is determined by the highest total sales amount, calculated as: total_paid = unitprice * quantity. 
# A negative quantity indicates a return or cancellation (the invoice number begins with 'C'. 
# To calculate sales, ignore returns and cancellations. Output the month, description of the item, and the total amount paid.

# Input DataFrame -  online_retail
# Expected Output Type - pandas.DataFrame

# Import your libraries
import pandas as pd

# Exclude returned or cancelled orders (invoice numbers starting with 'C')
sales = online_retail.loc[
    ~online_retail["invoiceno"].str.startswith("C", na=False)
].copy()

# Extract month and calculate the sales amount for each transaction
sales["month"] = sales["invoicedate"].dt.month
sales["total_paid"] = sales["quantity"] * sales["unitprice"]

# Calculate total sales for each product within each month
monthly_sales = (
    sales.groupby(["month", "description"], as_index=False)["total_paid"]
    .sum()
)

# Rank products by sales amount within each month
monthly_sales["rank"] = (
    monthly_sales.groupby("month")["total_paid"]
    .rank(method="dense", ascending=False)
)

# Return the best-selling product(s) for each month
result = (
    monthly_sales.loc[
        monthly_sales["rank"] == 1,
        ["month", "description", "total_paid"],
    ]
    .sort_values("month")
    .reset_index(drop=True)
)
