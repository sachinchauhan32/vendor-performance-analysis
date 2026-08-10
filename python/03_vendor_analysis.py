import pandas as pd
file = r"D:\Vendor_Performance_Analysis\data\cleaned\sales_cleaned.csv"
df = pd.read_csv(file)
# print(df.head())
# print(df.shape)
# print(df.columns)
df['SalesDate'] = pd.to_datetime(df['SalesDate'])
df['Month'] = df['SalesDate'].dt.month_name()
MonthlySales = df.groupby('Month',observed=True)['SalesDollars'].sum().sort_values(ascending=False)
print("====Monthly Sale===\n", MonthlySales)

VendorAnalysis = df.groupby('VendorName').agg(
  TotalSales = ('SalesDollars','sum'),
  TotalQuantity = ('SalesQuantity', 'sum'),
  AveragePrice = ('SalesPrice', 'mean'),
  BrandCount = ('Brand', 'nunique'),
  ProductCount = ('Description', 'nunique')
)
VendorAnalysis['RevenuePerUnit'] = (VendorAnalysis['TotalSales'] / VendorAnalysis['TotalQuantity']).round(2)
# print(VendorAnalysis.head().round(2))

VendorAnalysis['SalesRank'] = (VendorAnalysis['TotalSales'].rank(ascending=False, method='dense'))
VendorAnalysis['QuantityRank'] = (VendorAnalysis['TotalQuantity'].rank(ascending=False, method='dense'))
VendorAnalysis['OverAllRank'] = (VendorAnalysis[['SalesRank', 'QuantityRank']].mean(axis=1))
VendorAnalysis = VendorAnalysis.sort_values(by='OverAllRank')
# print("=====Top 10 Vendors====\n",VendorAnalysis.head(10))
TopTenVendors = VendorAnalysis.sort_values(by = 'TotalSales', ascending= False)
# print("===Top 10 Vendor by Sales===\n", TopTenVendors.head(10))
BottomTenVendors = VendorAnalysis.sort_values(by = 'TotalSales', ascending= True)
# print("===Bottom 10 Vendor by Sales===\n", BottomTenVendors.head(10))

output = r"D:\Vendor_Performance_Analysis\data\analysis\vendor_performance.csv"
VendorAnalysis.to_csv(output, index =  True)
print("Vendor Analysis Exported Successfully ")

monthly_output = r"D:\Vendor_Performance_Analysis\data\analysis\monthly_sales.csv"
MonthlySales.to_csv(monthly_output, index =  True)
print("Monthly Analysis Exported Successfully")
