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
