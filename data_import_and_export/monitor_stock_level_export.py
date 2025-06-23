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
JOIN Product P ON I.Product_ID = P.Product_ID;
"""

# STEP 3: Execute and fetch to a DataFrame
df = pd.read_sql(query, conn)

# STEP 4: Export to CSV
df.to_csv("monitor_stock_level.csv", index=False)
print("✅ Reorder points exported to 'monitor_stock_level.csv'")

# STEP 5: Close connection
conn.close()

