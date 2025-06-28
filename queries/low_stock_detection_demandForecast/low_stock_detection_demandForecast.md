# 📊 Inventory vs Demand Forecast Query

This SQL query retrieves the **latest inventory levels** for each product in each store and region, and compares them against the **demand forecast**. It filters only those records where the **inventory level is less than the expected demand**, indicating potential **stockouts** or need for **replenishment**.

## ✅ Objective

Identify products that are **understocked** based on forecasted demand.

## 🛠️ Query Logic

```sql
SELECT 
    I.Store_ID,
    I.Region,
    I.Product_ID,
    P.Category,
    I.Inventory_Level,
    F.Demand_Forecast,
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
 AND I.Date = Latest.MaxDate
JOIN Forecast F
  ON I.Store_ID = F.Store_ID
 AND I.Region = F.Region
 AND I.Product_ID = F.Product_ID
 AND I.Date = F.Date
JOIN Product P ON I.Product_ID = P.Product_ID
WHERE I.Inventory_Level < F.Demand_Forecast;
```
