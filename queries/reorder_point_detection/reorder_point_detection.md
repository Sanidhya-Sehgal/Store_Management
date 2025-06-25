# 📦 Reorder Point Detection

This document explains how to calculate the **reorder point** for each product, taking into account average sales and seasonality, using SQL.

---

## 📝 Query: Calculate Reorder Point with Seasonality Buffer

```sql
SELECT 
    I.Product_ID,
    E.Seasonality,
    ROUND(AVG(I.Units_Sold), 2) AS Avg_Units_Sold,
    
    -- Compute Seasonal Buffer based on Avg Units Sold
    CASE 
        WHEN ROUND(AVG(I.Units_Sold), 2) > 100 THEN 15
        WHEN ROUND(AVG(I.Units_Sold), 2) >= 50 THEN 10
        ELSE 0
    END AS Seasonal_Buffer,

    -- Final Reorder Point = Avg * 3 + Buffer
    ROUND(AVG(I.Units_Sold)*3 + 
        CASE 
            WHEN ROUND(AVG(I.Units_Sold), 2) > 100 THEN 15
            WHEN ROUND(AVG(I.Units_Sold), 2) >= 50 THEN 10
            ELSE 0
        END, 2) AS Reorder_Point

FROM Inventory I
JOIN Environment E ON I.Date = E.Date
GROUP BY I.Product_ID, E.Seasonality
ORDER BY I.Product_ID, E.Seasonality;
```