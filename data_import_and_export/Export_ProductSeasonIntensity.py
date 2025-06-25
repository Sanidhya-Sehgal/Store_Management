import mysql.connector
import pandas as pd

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Osho*2005",
    database="StoreManagement"
)

# Query to fetch the table
query = "SELECT * FROM ProductSeasonIntensity"

# Read into DataFrame
df = pd.read_sql(query, conn)

# Export to CSV
csv_path = "ProductSeasonIntensity_Export.csv"
df.to_csv(csv_path, index=False)

print(f"✅ Exported successfully to {csv_path}")

# Close connection
conn.close()

