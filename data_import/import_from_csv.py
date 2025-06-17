import pandas as pd
import mysql.connector

def safe_date(val):
    try:
        return pd.to_datetime(val).date()
    except:
        return None

# STEP 1: Load the CSV file
df = pd.read_csv("inventory_forecasting.csv")

# Clean up column names if needed
df.columns = df.columns.str.strip()

# STEP 2: Parse Date
df['Date'] = df['Date'].apply(safe_date)
df = df.dropna(subset=['Date'])

# STEP 3: Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Osho*2005",      # Change this to your MySQL password
    database="StoreManagement"       # Change this to your MySQL database name
)
cursor = conn.cursor()

# STEP 4: Insert into Store table
store_data = df[['Store ID', 'Region']].drop_duplicates()
for _, row in store_data.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Store (Store_ID, Region)
        VALUES (%s, %s)
    """, (row['Store ID'], row['Region']))

# STEP 5: Insert into Product table
product_data = df[['Product ID', 'Category']].drop_duplicates()
for _, row in product_data.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Product (Product_ID, Category)
        VALUES (%s, %s)
    """, (row['Product ID'], row['Category']))

# STEP 6: Insert into Environment table
env_data = df[['Date', 'Weather Condition', 'Holiday/Promotion', 'Seasonality']].drop_duplicates()
for _, row in env_data.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Environment (Date, Weather_Condition, Holiday_Promotion, Seasonality)
        VALUES (%s, %s, %s, %s)
    """, (
        row['Date'],
        row['Weather Condition'],
        int(row['Holiday/Promotion']),
        row['Seasonality']
    ))

# STEP 7: Insert into Pricing table
for _, row in df.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Pricing (Date, Store_ID, Region, Product_ID, Price, Discount, Competitor_Pricing)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row['Date'],
        row['Store ID'],
        row['Region'],
        row['Product ID'],
        float(row['Price']),
        int(row['Discount']),
        float(row['Competitor Pricing'])
    ))

# STEP 8: Insert into Inventory table
for _, row in df.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Inventory (Date, Store_ID, Region, Product_ID, Inventory_Level, Units_Sold, Units_Ordered)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row['Date'],
        row['Store ID'],
        row['Region'],
        row['Product ID'],
        int(row['Inventory Level']),
        int(row['Units Sold']),
        int(row['Units Ordered'])
    ))

# STEP 9: Insert into Forecast table
for _, row in df.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO Forecast (Date, Store_ID, Region, Product_ID, Demand_Forecast)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        row['Date'],
        row['Store ID'],
        row['Region'],
        row['Product ID'],
        float(row['Demand Forecast'])
    ))

# STEP 10: Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ Data successfully imported into all tables!")
