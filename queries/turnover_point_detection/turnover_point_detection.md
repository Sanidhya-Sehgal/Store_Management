# 🔄 Inventory Turnover Point Detection

This document explains how to calculate the **inventory turnover rate** for each store, region, and product category, and classify the turnover as High, Medium, or Low.

---

## 📝 Query: Calculate Inventory Turnover Rate and Category

```sql
SELECT 
    i.Store_ID,
    i.Region,
    p.Category,
    SUM(i.Units_Sold) AS Total_Units_Sold,
    ROUND(AVG(i.Inventory_Level), 2) AS Avg_Inventory,
    ROUND(SUM(i.Units_Sold) / AVG(i.Inventory_Level), 2) AS Turnover_Rate,

    CASE
        WHEN (SUM(i.Units_Sold) / AVG(i.Inventory_Level)) >= 1.5 THEN 'High'
        WHEN (SUM(i.Units_Sold) / AVG(i.Inventory_Level)) >= 0.8 THEN 'Medium'
        ELSE 'Low'
    END AS Turnover_Category

FROM 
    Inventory i
JOIN 
    Product p ON i.Product_ID = p.Product_ID
GROUP BY 
    i.Store_ID, i.Region, p.Category
ORDER BY 
    i.Store_ID, p.Category;
    ```