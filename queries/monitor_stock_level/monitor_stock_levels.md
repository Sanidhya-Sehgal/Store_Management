# Monitoring Stock Levels

This document demonstrates how to monitor and analyze stock levels across stores and regions using SQL queries and visual screenshots.

---

## 1. Get Latest Stock Date for Each Product-Store Combination

```sql
SELECT Store_ID, Region, Product_ID, MAX(Date) AS MaxDate
FROM Inventory
GROUP BY Store_ID, Region, Product_ID;
```

This query gives us the latest stock date for each product-store combination.

---

## 2. Get Complete Inventory Data for the Latest Date

Join the inventory table with the latest date for each product-store combination:

```sql
SELECT 
    I.Store_ID,
    I.Region,
    I.Product_ID,
    I.Inventory_Level,
    I.Date
FROM Inventory I
JOIN (
    SELECT Store_ID, Region, Product_ID, MAX(Date) AS MaxDate
    FROM Inventory
    GROUP BY Store_ID, Region, Product_ID
) AS Latest 
ON I.Store_ID = Latest.Store_ID
   AND I.Region = Latest.Region
   AND I.Product_ID = Latest.Product_ID
   AND I.Date = Latest.MaxDate;
```

---

## 3. Add Product Category Using JOIN

To group stock levels by category, join with the Product table:

```sql
SELECT 
    I.Store_ID,
    I.Region,
    P.Category,
    I.Product_ID,
    I.Inventory_Level,
    I.Date AS Latest_Stock_Date
FROM Inventory I
JOIN (
    SELECT Store_ID, Region, Product_ID, MAX(Date) AS MaxDate
    FROM Inventory
    GROUP BY Store_ID, Region, Product_ID
) AS Latest 
  ON I.Store_ID = Latest.Store_ID
 AND I.Region = Latest.Region
 AND I.Product_ID = Latest.Product_ID
 AND I.Date = Latest.MaxDate
JOIN Product P ON I.Product_ID = P.Product_ID;
```

---
## 5. Aggregate Stock Levels by Store, Region, and Category

Now, we can aggregate the stock levels by `Store_ID`, `Region`, and `Category` to get the total and average stock levels:

```sql
SELECT 
    Store_ID,
    Region,
    Category,
    SUM(Inventory_Level) AS Total_Stock_Level,
    AVG(Inventory_Level) AS Avg_Stock_Per_Product
FROM (
    SELECT 
        I.Store_ID,
        I.Region,
        P.Category,
        I.Product_ID,
        I.Inventory_Level,
        I.Date AS Latest_Stock_Date
    FROM Inventory I
    JOIN (
        SELECT Store_ID, Region, Product_ID, MAX(Date) AS MaxDate
        FROM Inventory
        GROUP BY Store_ID, Region, Product_ID
    ) AS Latest 
    ON I.Store_ID = Latest.Store_ID
    AND I.Region = Latest.Region
    AND I.Product_ID = Latest.Product_ID
    AND I.Date = Latest.MaxDate
    JOIN Product P ON I.Product_ID = P.Product_ID
) AS LatestInventory
GROUP BY Store_ID, Region, Category
ORDER BY Store_ID, Category;
```
