# Low Stock Detection

This document explains how to detect products that are at risk of going out of stock by comparing current inventory levels with demand forecasts.

---

## Logic

If the **Inventory Level** is less than the **Demand Forecast**, the product might soon go out of stock.

---

## SQL Query: Detect Low Stock Products

The following query retrieves the latest inventory and forecast data for each product, and identifies those where inventory is below forecasted demand:

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
    SELECT 
        Store_ID, 
        Region, 
        Product_ID, 
        MAX(Date) AS MaxDate
    FROM Inventory
    GROUP BY 
        Store_ID, 
        Region, 
        Product_ID
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
JOIN Product P 
    ON I.Product_ID = P.Product_ID
WHERE I.Inventory_Level < F.Demand_Forecast;
```

---
## 4. Low Stock Data Screenshots

Below are screenshots showing the low stock detection results:

![low stock data screenshots](low_stock_level_images/Screenshot%20from%202025-06-18%2000-46-21.png)
![low stock data screenshots](low_stock_level_images/Screenshot%20from%202025-06-18%2000-46-31.png)
![low stock data screenshots](low_stock_level_images/Screenshot%20from%202025-06-18%2000-46-53.png)

---
## Explanation

- **Latest Inventory:** Uses a subquery to get the most recent inventory record for each product in each store and region.
- **Forecast Join:** Joins the latest inventory with the corresponding demand forecast for the same date.
- **Product Info:** Joins with the product table to include category information.
- **Low Stock Condition:** Filters for products where the inventory level is less than the demand forecast.

---

## Usage

Use this query to generate alerts or reports for products that may require restocking soon.