-- This gives us the latest stock date for each product-store combination.

-- SELECT Store_ID, Region, Product_ID, MAX(Date) AS MaxDate
-- FROM Inventory
-- GROUP BY Store_ID, Region, Product_ID;
----------------------------------------------------------------------------------------------------------------------------------------
-- Get Complete Inventory Data for That Latest Date, joining the inventory table with the latest date for each product-store combination.

-- SELECT 
--     I.Store_ID,
--     I.Region,
--     I.Product_ID,
--     I.Inventory_Level,
--     I.Date
-- FROM Inventory I
-- JOIN (
--     SELECT Store_ID, Region, Product_ID, MAX(Date) AS MaxDate
--     FROM Inventory
--     GROUP BY Store_ID, Region, Product_ID
-- ) AS Latest 
-- ON I.Store_ID = Latest.Store_ID
--    AND I.Region = Latest.Region
--    AND I.Product_ID = Latest.Product_ID
--    AND I.Date = Latest.MaxDate;
---------------------------------------------------------------------------------------------------------------------------
-- Add Product Category Using JOIN

To group stock levels by category, join with the Product table:

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

--------------------------------------------------------------------------------------------------------------------------------------------------------

