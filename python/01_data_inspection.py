import pandas as pd

file = r"D:\Vendor_Performance_Analysis\data\raw\sales.csv"
df = pd.read_csv(file)
# print("Top 5 Rows")
# print(df.head(5))
# print("==========All Columns of Data===========")
# print(df.columns)
# print("=========Total Rows & Columns of the data==========")
# print(df.shape)
# print("==========Data Types of Columns=========")
# print(df.dtypes)
# print("==========Calculating Duplicates Values========")
# print(df.duplicated().sum())
# print("==========Checking Null Values==============")
# print(df.isnull().sum())


# total_rows = 0
# total_duplicates = 0
# null_values = {}

# for chunk in pd.read_csv(file, chunksize= 100000):
#   total_rows += len(chunk)
#   total_duplicates = chunk.duplicated().sum()
#   null_counts = chunk.isnull().sum()

#   for column, count in null_counts.items():
#     null_values[column] = null_values.get(column, 0) +  count

# print("=========Full Dataset Result==========")
# print("== total rows ==\n", total_rows)
# print("== Total Duplicates Values ==\n", total_duplicates)
# print("== null values == \n", null_values)

# print(df.describe().round(2))
# print(df.nunique())

# print(df.min().SalesDate)
# print(df.max().SalesDate)
print(df.dtypes.SalesDate)
df['SalesDate'] = pd.to_datetime(df['SalesDate'])
# print(df.dtypes.SalesDate)

DailySales = df.groupby('SalesDate', as_index=False)['SalesDollars'].sum()
df['Month'] = df['SalesDate'].dt.month_name()
month_order = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]
df['Month'] = pd.Categorical(
    df['Month'],
    categories=month_order,
    ordered=True
)
MonthlySales = df.groupby(
    'Month',
    observed=True
)['SalesDollars'].sum()

# print(MonthlySales)
MonthlyQuantity = df.groupby('Month')['SalesQuantity'].sum()
# print("== Month wise Quantity == ",MonthlyQuantity)
AnnualTotal = df['SalesDollars'].sum().round(2)
# print("== Annual Total ==",AnnualTotal)



VendorTotalSale = df.groupby('VendorName')['SalesDollars'].sum().round(2)
# print(VendorTotalSale)

VendorTotalSale = VendorTotalSale.sort_values(ascending=False)
# print(VendorTotalSale.head(10))

QuantitySoldByVendor = df.groupby('VendorName')['SalesQuantity'].sum()
QuantitySoldByVendor = QuantitySoldByVendor.sort_values(ascending=False)
# print(QuantitySoldByVendor.head(10))

# print(df.columns)

VendorAveragePrice = df.groupby('VendorName')['SalesPrice'].mean().round(2)
VendorAveragePrice = VendorAveragePrice.sort_values(ascending=False)
# print(VendorAveragePrice.head(10))

BrandTotal = df.groupby('VendorName')['Brand'].nunique()
BrandTotal = BrandTotal.sort_values(ascending=False)
# print(BrandTotal.head(10))

ProductCount = df.groupby('VendorName')['Description'].nunique()
ProductCount = ProductCount.sort_values(ascending=False)
# print(ProductCount.head(10))

VendorsPerformance = pd.concat([VendorTotalSale,QuantitySoldByVendor,VendorAveragePrice,BrandTotal,ProductCount], axis=1)
# print(VendorsPerformance)

VendorsPerformance = pd.concat([VendorTotalSale,QuantitySoldByVendor,VendorAveragePrice,BrandTotal,ProductCount], axis=1)
VendorsPerformance = VendorsPerformance.sort_values(by = 'SalesDollars', ascending=False)
# print(VendorsPerformance.head(10))

df["VendorName"] = df["VendorName"].str.strip().str.upper()

RevenuePerUnit = VendorTotalSale / QuantitySoldByVendor
RevenuePerUnit.name = 'RevenuePerUnit'
VendorsPerformance = pd.concat(
    [
        VendorTotalSale,
        QuantitySoldByVendor,
        RevenuePerUnit,
        VendorAveragePrice,
        BrandTotal,
        ProductCount
    ],
    axis=1
)
VendorsPerformance = VendorsPerformance.sort_values( by='RevenuePerUnit', ascending=False )
# print(VendorsPerformance.head(10))

BottomVendors = VendorsPerformance.sort_values(by = 'SalesDollars', ascending=True).head(10)
# print(BottomVendors.head(10))

TopVendors = VendorsPerformance.head(10)
# print("====Top Vendors===\n", TopVendors,"\n===Bottom Vendors===\n", BottomVendors.head(10))

TopVendorsAvg = TopVendors.mean().round(2)
BottomVendorsAvg = BottomVendors.mean().round(2)
# print("=====Average of Top Vendors======\n", TopVendorsAvg, "=====Average of Bottom Vendors======\n", BottomVendorsAvg)

PercentageDifference =  ((TopVendorsAvg - BottomVendorsAvg ) / BottomVendorsAvg ) * 100
# print("==========Percentage Difference====== \n", PercentageDifference.round(2))

# AllVendorsCalculation = pd.concat([VendorTotalSale,QuantitySoldByVendor,RevenuePerUnit,VendorAveragePrice,BrandTotal,ProductCount], axis=1)

# Comparing = df.groupby('VendorsPerformance', 'BottomVendors')[AllVendorsCalculation]
# print(Comparing.head(10))

VendorsPerformance = VendorsPerformance.reset_index()

VendorsPerformance['SalesRank'] = VendorsPerformance['SalesDollars'].rank(ascending=False)

VendorsPerformance['QuantityRank'] = VendorsPerformance['SalesQuantity'].rank(ascending=False)

VendorsPerformance['RevenueRank'] = VendorsPerformance['RevenuePerUnit'].rank(ascending=False)

VendorsPerformance['BrandRank'] = VendorsPerformance['Brand'].rank(ascending=False)

VendorsPerformance['ProductRank'] = VendorsPerformance['Description'].rank(ascending=False)

VendorsPerformance['OverallRank'] = VendorsPerformance[
    ['SalesRank', 'QuantityRank', 'RevenueRank', 'BrandRank', 'ProductRank']
].mean(axis=1)
VendorsPerformance = VendorsPerformance.sort_values( by='OverallRank',ascending=True
)
VendorsPerformance['FinalRank'] = VendorsPerformance['OverallRank'].rank(ascending=True, method='dense')
print(VendorsPerformance['FinalRank'].head(10))







VendorsPerformance.to_csv(
    "data/analysis/vendor_performance.csv",
    index=False
)

vendor = pd.read_csv("data/analysis/vendor_performance.csv")

print(vendor.columns.tolist())

# import pandas as pd

# begin_df = pd.read_csv("data/raw/begin_inventory.csv")
# end_df = pd.read_csv("data/raw/end_inventory.csv")

# print("BEGIN INVENTORY")
# print(begin_df.dtypes)
# print(begin_df.head())

# print("\nEND INVENTORY")
# print(end_df.dtypes)
# print(end_df.head())



