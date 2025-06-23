# 🧮 Stock Level Classification SQL Query

This query fetches the **latest inventory level** of each product, compares it to the **average inventory level of its category**, and classifies each product's stock status as **Critical**, **Warning**, or **Safe**.

---

## 📌 Step 1: Get Latest Inventory Per Product

```sql
WITH Latest_Inventory AS (
    SELECT 
        I.Store_ID,
        I.Region,
        I.Product_ID,
        P.Category,
        I.Inventory_Level,
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
    JOIN Product P 
        ON I.Product_ID = P.Product_ID
)
```

### 🔍 Explanation:
- `Latest_Inventory` CTE extracts the most **recent inventory record** for each product across store and region.
- It uses a subquery to find the **maximum (latest) date** for each product.
- Then joins back to the `Inventory` table to fetch the full row for that latest date.
- Also joins with the `Product` table to include the product's **category**.

---

## 📌 Step 2: Calculate Category-Wise Average Inventory

```sql
Category_Avg AS (
    SELECT 
        Category, 
        AVG(Inventory_Level) AS Avg_Category_Inventory
    FROM Latest_Inventory
    GROUP BY Category
)
```

### 🔍 Explanation:
- Calculates the **average inventory level** for each `Category` using the output from `Latest_Inventory`.

---

## 📌 Step 3: Classify Stock Status (Critical / Warning / Safe)

```sql
SELECT 
    LI.Store_ID,
    LI.Region,
    LI.Product_ID,
    LI.Category,
    LI.Inventory_Level,
    CA.Avg_Category_Inventory,
    CASE 
        WHEN LI.Inventory_Level < 0.5 * CA.Avg_Category_Inventory THEN 'Critical'
        WHEN LI.Inventory_Level < 0.8 * CA.Avg_Category_Inventory THEN 'Warning'
        ELSE 'Safe'
    END AS Stock_Status
FROM Latest_Inventory LI
JOIN Category_Avg CA 
    ON LI.Category = CA.Category;
```

### 🔍 Explanation:
- Joins `Latest_Inventory` (per-product latest stock) with `Category_Avg` (category average inventory).
- Uses a `CASE` block to assign a **stock status**:
  - `< 50%` of category average → **Critical**
  - `< 80%` of category average → **Warning**
  - Otherwise → **Safe**

---

## final code :

```sql
WITH Latest_Inventory AS (
    SELECT 
        I.Store_ID,
        I.Region,
        I.Product_ID,
        P.Category,
        I.Inventory_Level,
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
    JOIN Product P 
        ON I.Product_ID = P.Product_ID
),
Category_Avg AS (
    SELECT 
        Category, 
        AVG(Inventory_Level) AS Avg_Category_Inventory
    FROM Latest_Inventory
    GROUP BY Category
)
SELECT 
    LI.Store_ID,
    LI.Region,
    LI.Product_ID,
    LI.Category,
    LI.Inventory_Level,
    CA.Avg_Category_Inventory,
    CASE 
        WHEN LI.Inventory_Level < 0.5 * CA.Avg_Category_Inventory THEN 'Critical'
        WHEN LI.Inventory_Level < 0.8 * CA.Avg_Category_Inventory THEN 'Warning'
        ELSE 'Safe'
    END AS Stock_Status
FROM Latest_Inventory LI
JOIN Category_Avg CA 
    ON LI.Category = CA.Category;

```

## ✅ Output Columns:

| Column Name             | Description                              |
|-------------------------|------------------------------------------|
| Store_ID                | Store identifier                         |
| Region                  | Geographical region                      |
| Product_ID              | Unique product ID                        |
| Category                | Product category                         |
| Inventory_Level         | Most recent inventory count              |
| Avg_Category_Inventory  | Average inventory for that category      |
| Stock_Status            | One of: `Critical`, `Warning`, or `Safe` |