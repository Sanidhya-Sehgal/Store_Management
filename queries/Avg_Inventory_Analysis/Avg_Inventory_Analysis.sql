-- Here, we aggregate the stock levels by Store_ID, Region, and Category to get the total and average stock levels.

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
