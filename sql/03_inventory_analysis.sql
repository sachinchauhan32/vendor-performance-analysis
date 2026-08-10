CREATE TABLE begin_inventory(
InventoryId VARCHAR(50),
Store INT,
City TEXT,
Brand INT,
Description TEXT,
Size VARCHAR(20),
onHand INT,
Price NUMERIC(10,2),
startDate DATE

);

CREATE TABLE end_inventory (
InventoryId VARCHAR(50),
Store INT,
City TEXT,
Brand INT,
Description TEXT,
Size VARCHAR(20),
onHand INT,
Price NUMERIC(10,2),
endDate DATE

);
--===================================================checking begin inventory 
SELECT * FROM begin_inventory
LIMIT 10;

SELECT COUNT(*)FROM begin_inventory;
--===================================================checking ending inventory
SELECT * FROM end_inventory
LIMIT 10;

SELECT COUNT(*)FROM end_inventory;

--===================================================Beginning VS Ending Inventory Comparison
SELECT 	
	b.inventoryid, b.description, b.store, b.onhand AS beginning_inventory,
	e.onhand AS ending_inventory,
	(e.onhand - b.onhand) AS inventory_change
FROM begin_inventory b
INNER JOIN end_inventory e
ON b.inventoryid = e.inventoryid
ORDER BY inventory_change DESC;

--===================================================Products Close to Stock Out
SELECT inventoryid,store, description, onhand
FROM end_inventory
WHERE onhand <= 5
ORDER BY onhand;


--===================================================Overstocked Products
SELECT inventoryid, store, description, onhand
FROM end_inventory
ORDER BY onhand DESC;


--===================================================Inventory Value
SELECT InventoryId,Description,Store,onHand,Price,ROUND(onHand * Price,2) AS Inventory_Value
FROM end_inventory
ORDER BY Inventory_Value DESC;

--===================================================Store-wise Inventory Value
SELECT store, ROUND(onHand * price,2) AS inventory_value
FROM end_inventory
ORDER BY inventory_value DESC;

--===================================================Brands with Highest Inventory
SELECT brand, SUM(onhand) AS inventory_stock
FROM end_inventory
GROUP BY brand
ORDER BY inventory_stock DESC
LIMIT 10;

--===================================================Inventory Growth %
SELECT b.inventoryid, b.description, b.onhand AS beginning,
		e.onhand AS ending,
		ROUND(((e.onhand - b.onhand) * 100.0) / NULLIF(B.onhand, 0),2) AS growth_percentage
FROM begin_inventory b
INNER JOIN end_inventory e
ON b.inventoryid = e.inventoryid
ORDER BY growth_percentage DESC;



