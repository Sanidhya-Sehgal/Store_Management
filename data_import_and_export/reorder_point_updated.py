import mysql.connector
import pandas as pd

# STEP 1: Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Osho*2005",
    database="StoreManagement"
)

# STEP 2: Define the query with dynamic reorder point logic
query = """
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
"""

# STEP 3: Execute and fetch to a DataFrame
df = pd.read_sql(query, conn)

# STEP 4: Export to CSV
df.to_csv("reorder_points_updated.csv", index=False)
print("✅ Reorder points exported to 'reorder_points_updated.csv'")

# STEP 5: Close connection
conn.close()

