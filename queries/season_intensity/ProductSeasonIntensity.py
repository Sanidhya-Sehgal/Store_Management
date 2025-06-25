import mysql.connector
import pandas as pd

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Osho*2005",
    database="StoreManagement"
)
cursor = conn.cursor()

# Query to get avg units sold per store/product/season
query = """
SELECT 
    I.Store_ID,
    I.Region,
    I.Product_ID,
    P.Category,
    E.Seasonality,
    ROUND(AVG(I.Units_Sold), 2) AS Avg_Units_Sold
FROM Inventory I
JOIN Environment E ON I.Date = E.Date
JOIN Product P ON I.Product_ID = P.Product_ID
GROUP BY I.Store_ID, I.Region, I.Product_ID, P.Category, E.Seasonality
"""
df = pd.read_sql(query, conn)

# Define classification function
def classify(units):
    if units > 100:
        return "High"
    elif units >= 50:
        return "Moderate"
    else:
        return "Low"

# Apply classification
df["Season_Intensity"] = df["Avg_Units_Sold"].apply(classify)

# Optional: Clear old data
cursor.execute("DELETE FROM ProductSeasonIntensity")

# Insert data into new table
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO ProductSeasonIntensity
        (Store_ID, Region, Product_ID, Category, Seasonality, Avg_Units_Sold, Season_Intensity)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row["Store_ID"],
        row["Region"],
        row["Product_ID"],
        row["Category"],
        row["Seasonality"],
        row["Avg_Units_Sold"],
        row["Season_Intensity"]
    ))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ ProductSeasonIntensity table updated.")

