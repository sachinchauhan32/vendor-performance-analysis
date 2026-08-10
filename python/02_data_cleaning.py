import pandas as pd
file = r"D:\Vendor_Performance_Analysis\data\raw\sales.csv"
df = pd.read_csv(file)
# print(df.shape)
# print(df.dtypes)
# print(df.isnull().sum())
# print(df.duplicated().sum())
# print("====Before Conversion=====\n",df['SalesDate'].dtypes)
df['SalesDate'] = pd.to_datetime(df['SalesDate'], errors='coerce')
# print("====After Conversion=====\n",df['SalesDate'].dtypes)

numeric_columns = ['SalesQuantity','SalesDollars','SalesPrice','Volume','Classification','ExciseTax']
# print("======Important numerics columns========\n",df[numeric_columns].dtypes)
print("======Checking Missing Values=========")
print(df.isnull().sum)

print("=======Checking Duplicates Values=========")
print(df.duplicated().sum())
print(df.drop_duplicates())
print(df.duplicated().sum())

print("====Checking Invalid Numerical Values======")
print("====Negative Sales Quantity===\n", (df['SalesQuantity'] < 0).sum())
print("====Negative Dollars ===\n", (df['SalesDollars'] < 0).sum())
print("====Negative Price===\n", (df['SalesPrice'] < 0).sum())
print("====Negative Volume===\n", (df['Volume'] < 0).sum())
print("====Negative Excise Tax===\n", (df['ExciseTax'] < 0).sum())

print("===Final Shape of the Data===\n", df.shape)

# output_file = r"D:\Vendor_Performance_Analysis\data\cleaned\sales_cleaned.csv"
# df.to_csv(output_file, index=False)
# print("Cleaned File Saved Successfully")  

# ===== CLEAN PURCHASE DATA =====

purchase_df = pd.read_csv("data/raw/purchases.csv")

# Convert date columns
purchase_df["PODate"] = pd.to_datetime(purchase_df["PODate"])
purchase_df["ReceivingDate"] = pd.to_datetime(purchase_df["ReceivingDate"])
purchase_df["InvoiceDate"] = pd.to_datetime(purchase_df["InvoiceDate"])
purchase_df["PayDate"] = pd.to_datetime(purchase_df["PayDate"])

# Remove duplicates
purchase_df.drop_duplicates(inplace=True)

# Export cleaned file
purchase_df.to_csv(
    "data/cleaned/purchases_cleaned.csv",
    index=False
)

print("Purchase data cleaned and exported successfully.")