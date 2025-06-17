import mysql.connector

conn = mysql.connector.connect(
    user='root',
    password='Osho*2005',  
    host='localhost',
    database='StoreManagement'
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Store (
    Store_ID VARCHAR(10),
    Region VARCHAR(50),
    PRIMARY KEY (Store_ID, Region)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Product (
    Product_ID VARCHAR(10) PRIMARY KEY,
    Category VARCHAR(50)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Environment (
    Date DATE PRIMARY KEY,
    Weather_Condition VARCHAR(20),
    Holiday_Promotion BOOLEAN,
    Seasonality VARCHAR(20)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Pricing (
    Date DATE,
    Store_ID VARCHAR(10),
    Region VARCHAR(50),
    Product_ID VARCHAR(10),
    Price FLOAT,
    Discount INT,
    Competitor_Pricing FLOAT,
    PRIMARY KEY (Date, Store_ID, Region, Product_ID),
    FOREIGN KEY (Store_ID, Region) REFERENCES Store(Store_ID, Region),
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Inventory (
    Date DATE,
    Store_ID VARCHAR(10),
    Region VARCHAR(50),
    Product_ID VARCHAR(10),
    Inventory_Level INT,
    Units_Sold INT,
    Units_Ordered INT,
    PRIMARY KEY (Date, Store_ID, Region, Product_ID),
    FOREIGN KEY (Store_ID, Region) REFERENCES Store(Store_ID, Region),
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Forecast (
    Date DATE,
    Store_ID VARCHAR(10),
    Region VARCHAR(50),
    Product_ID VARCHAR(10),
    Demand_Forecast FLOAT,
    PRIMARY KEY (Date, Store_ID, Region, Product_ID),
    FOREIGN KEY (Store_ID, Region) REFERENCES Store(Store_ID, Region),
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
)
""")

conn.commit()
cursor.close()
conn.close()
