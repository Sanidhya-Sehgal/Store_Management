import mysql.connector
import pandas as pd

# STEP 1: Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Osho*2005",
    database="StoreManagement"
)

# Step 2: Define the query
query = """
SELECT 
    i.Store_ID,
    i.Region,
    p.Category,
    SUM(i.Units_Sold) AS Total_Units_Sold,
    ROUND(AVG(i.Inventory_Level), 2) AS Avg_Inventory,
    ROUND(SUM(i.Units_Sold) / AVG(i.Inventory_Level), 2) AS Turnover_Rate
FROM 
    Inventory i
JOIN 
    Product p ON i.Product_ID = p.Product_ID
GROUP BY 
    i.Store_ID, i.Region, p.Category
ORDER BY 
    i.Store_ID, p.Category;
"""

# Step 3: Load query result into a DataFrame
df = pd.read_sql(query, conn)

# Step 4: Export to CSV
df.to_csv("turnover_data.csv", index=False)

# Step 5: Close the connection
conn.close()

print("✅ Exported as turnover_data.csv")

