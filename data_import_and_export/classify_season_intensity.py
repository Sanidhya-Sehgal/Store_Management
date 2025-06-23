import mysql.connector
import pandas as pd

# Connect to DB
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Osho*2005",
    database="StoreManagement"
)
cursor = conn.cursor()

# Load Avg Units Sold per Product/Season
query = """
SELECT 
    I.Product_ID,
    E.Seasonality,
    ROUND(AVG(I.Units_Sold), 2) AS Avg_Units_Sold
FROM Inventory I
JOIN Environment E ON I.Date = E.Date
GROUP BY I.Product_ID, E.Seasonality
"""
df = pd.read_sql(query, conn)

# Classify Season Intensity
def classify(avg_units):
    if avg_units > 100:
        return "High"
    elif avg_units >= 50:
        return "Moderate"
    else:
        return "Low"

df["Season_Intensity"] = df["Avg_Units_Sold"].apply(classify)

# Print result
print(df)

# Insert into new table SeasonIntensity
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO SeasonIntensity (Product_ID, Seasonality, Avg_Units_Sold, Season_Intensity)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            Avg_Units_Sold = VALUES(Avg_Units_Sold),
            Season_Intensity = VALUES(Season_Intensity)
    """, (
        row["Product_ID"],
        row["Seasonality"],
        row["Avg_Units_Sold"],
        row["Season_Intensity"]
    ))

conn.commit()
cursor.close()
conn.close()

print("✅ Season intensity calculated and stored in SeasonIntensity table.")

