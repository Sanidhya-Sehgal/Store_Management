
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

"""

# STEP 3: Execute and fetch to a DataFrame
df = pd.read_sql(query, conn)

# STEP 4: Export to CSV
df.to_csv("turnover.csv", index=False)
print("✅ Reorder points exported to 'turnover.csv'")

# STEP 5: Close connection
conn.close()

