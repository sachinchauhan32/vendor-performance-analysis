CREATE TABLE purchases (

    InventoryId      VARCHAR(50),
    Store            INT,
    Brand            INT,
    Description      TEXT,
    Size             VARCHAR(30),
    VendorNumber     INT,
    VendorName       TEXT,
    PONumber         BIGINT,
    PODate           DATE,
    ReceivingDate    DATE,
    InvoiceDate      DATE,
    PayDate          DATE,
    PurchasePrice    NUMERIC(10,2),
    Quantity         INT,
    Dollars          NUMERIC(12,2),
    Classification   INT

);

SELECT COUNT(*) FROM purchases;

SELECT * FROM purchases
LIMIT 5;

--=======================================================Total Purchase Cost
SELECT SUM(Dollars) as total_purchase_cost
FROM purchases;

--=======================================================Total Puchase Quantity
SELECT SUM(Quantity) AS total_purchase_quantity
FROM purchases;

--=======================================================Average Purchase Price
SELECT ROUND(AVG(Purchaseprice::numeric),2) AS Avg_purchase_price
FROM purchases;

--=======================================================Total Vendors
SELECT COUNT(DISTINCT Vendorname) AS total_vendors
FROM purchases;

--=======================================================Total Brands Purchased
SELECT COUNT(DISTINCT Brand) AS total_brand_purchased
FROM purchases;

--=======================================================Total Products Purchased
SELECT COUNT(DISTINCT Description) AS total_product_purchased
FROM purchases;



--=======================================================Vendor wise Purchase Cost
SELECT Vendorname, SUM(purchaseprice) AS purchase_cost
FROM purchases
GROUP BY Vendorname
ORDER BY purchase_cost DESC;

--=======================================================Vendor wise Purchase Quantity
SELECT Vendorname, SUM(Quantity) AS purchase_quantity
FROM purchases
GROUP BY Vendorname
ORDER BY purchase_quantity DESC;

--=======================================================Vendor wise Average Purchase Price
SELECT Vendorname, ROUND(AVG(purchaseprice::numeric),2) AS purchase_price
FROM purchases
GROUP BY Vendorname
ORDER BY purchase_price DESC;

--=======================================================Vendor wise Brand Count
SELECT Vendorname, COUNT(DISTINCT Brand) AS brand_count
FROM purchases
GROUP BY Vendorname
ORDER BY brand_count DESC;

--=======================================================Vendor-wise Product Count
SELECT Vendorname, COUNT(DISTINCT Description) AS product_count
FROM purchases
GROUP BY vendorname
ORDER BY product_count DESC;

--=======================================================Cost Per Unit
SELECT Vendorname, ROUND(SUM(dollars) / SUM(quantity),2) AS cost_per_unit
FROM purchases
GROUP BY Vendorname
ORDER BY cost_per_unit DESC;

--=======================================================Top 10 Purchase Vendors
SELECT Vendorname, SUM(Dollars) AS top_purchase_vendor
FROM purchases
GROUP BY Vendorname
ORDER BY top_purchase_vendor DESC 
LIMIT 10;

--=======================================================Bottom 10 Purchase Vendors
SELECT Vendorname, SUM(Dollars) AS bottom_purchase_vendor
FROM purchases
GROUP BY Vendorname
ORDER BY bottom_purchase_vendor ASC
LIMIT 10;

--=======================================================Monthly Purchase Cost
SELECT TO_CHAR(podate, 'Month') AS month,
		SUM(Dollars) AS purchase_cost
FROM purchases
GROUP BY TO_CHAR(podate, 'Month'), DATE_TRUNC('month', podate)
ORDER BY DATE_TRUNC('month', podate);

--=======================================================Monthly Purchase Quantity
SELECT TO_CHAR(podate, 'Month') AS month,
		SUM(quantity) AS purchase_quantity
FROM purchases
GROUP BY TO_CHAR(podate, 'Month'), DATE_TRUNC('month', podate)
ORDER BY DATE_TRUNC('month', podate);

--=======================================================Monthly Average Purchase Price
SELECT TO_CHAR(podate, 'Month') AS month,
		ROUND(AVG(purchaseprice::numeric),2) AS purchase_price
FROM purchases
GROUP BY TO_CHAR(podate, 'Month'), DATE_TRUNC('month', podate)
ORDER BY DATE_TRUNC('month', podate);

--=======================================================Top Purchased Products
SELECT Description, SUM(Dollars) AS top_purchases_products
FROM purchases
GROUP BY Description
ORDER BY top_purchaseS_products DESC
LIMIT 10;

--=======================================================Most Purchased Brands
SELECT DISTINCT(Brand) AS unique_brand,
		SUM(Dollars) AS most_purchased_brand
FROM purchases
GROUP BY unique_brand
ORDER BY most_purchased_brand DESC
LIMIT 10;

--=======================================================Store-wise Purchase Cost
SELECT DISTINCT(Store) AS unique_store,
		SUM(Dollars) AS purchase_cost
FROM purchases
GROUP BY unique_store
ORDER BY purchase_cost DESC
LIMIT 10;

--=======================================================Store-wise Purchase Quantity
SELECT Store, SUM(quantity) AS purchase_quantity
FROM purchases
GROUP BY store
ORDER BY purchase_quantity DESC
LIMIT 10;

--=======================================================Vendors Above Average Purchase Cost
WITH Vendorsavg AS (
SELECT vendorname, AVG(Dollars) AS avg_purchase_cost
FROM purchases
GROUP BY vendorname
)
SELECT Vendorname, ROUND(avg_purchase_cost::numeric,2) AS avg_purchase 
FROM Vendorsavg
WHERE avg_purchase_cost > (SELECT AVG(Dollars) FROM purchases)
ORDER BY avg_purchase_cost DESC
LIMIT 10;

--=======================================================Vendors Below Average Purchase Cost
WITH Vendorsavg AS (
SELECT vendorname, AVG(Dollars) AS avg_purchase_cost
FROM purchases
GROUP BY vendorname
)
SELECT Vendorname, ROUND(avg_purchase_cost::numeric,2) AS avg_purchase 
FROM Vendorsavg
WHERE avg_purchase_cost > (SELECT AVG(Dollars) FROM purchases)
ORDER BY avg_purchase_cost ASC
LIMIT 10;

--=======================================================Vendor Contribution %
SELECT VendorName,
    ROUND(SUM(Dollars::numeric), 2) AS Purchase_Cost,
    ROUND((SUM(Dollars::numeric) * 100.0) / SUM(SUM(Dollars::numeric)) OVER (),2) AS Contribution_Percent
FROM purchases
GROUP BY VendorName
ORDER BY Purchase_Cost DESC;

--=======================================================Purchase Category
SELECT Vendorname, SUM(Dollars) AS purchase_cost,
		CASE
		WHEN SUM(Dollars) > 10000000 THEN 'High_Purchase'
		WHEN SUM(Dollars) > 5000000  THEN 'Medium_Purchase'
		ELSE 'Low_Purchase'
		END AS purchase_category
FROM purchases
GROUP BY Vendorname
ORDER BY purchase_cost DESC;


--=======================================================Vendor Rank by Purchase Cost
SELECT Vendorname, ROUND(SUM(Dollars),2) AS purchase_cost,
DENSE_RANK() OVER( ORDER BY SUM(Dollars) DESC) AS purchase_rank
FROM purchases
GROUP BY vendorname;

--=======================================================Assigning Row Number to Vendors acc to purchase cost
SELECT Vendorname, ROUND(SUM(Dollars),2) AS purchase_cost,
ROW_NUMBER() OVER( ORDER BY SUM(Dollars) DESC) AS row_number
FROM purchases
GROUP BY vendorname;

--=======================================================Running Purchase Cost
SELECT DATE_TRUNC('month', podate) AS month,
		ROUND(SUM(Dollars),2) AS purchase_cost,
		ROUND(SUM(SUM(Dollars)) OVER( ORDER BY DATE_TRUNC('month', podate)),2) as running_total
FROM purchases
GROUP BY month
ORDER BY month;

--=======================================================Moving Average Purchase Cost
SELECT DATE_TRUNC('month', podate) AS month,
		ROUND(SUM(Dollars),2) AS purchase_cost,
		ROUND(AVG(SUM(Dollars)) OVER( ORDER BY DATE_TRUNC('month', podate) ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) as moving_average
FROM purchases
GROUP BY month
ORDER BY month;

--=======================================================Vendor Purchase View
CREATE VIEW vendor_purchase_summary AS 
SELECT vendorname, ROUND(SUM(Dollars),2) AS purchase_cost,
SUM(Quantity) AS purchase_quantity,
ROUND(AVG(purchaseprice),2) AS avg_purchase_price
FROM purchases
GROUP BY vendorname;

SELECT * FROM vendor_purchase_summary
LIMIT 20;


--=======================================================Query Performance

EXPLAIN ANALYZE 
SELECT VendorName, SUM(Dollars)
FROM purchases
GROUP BY VendorName;



