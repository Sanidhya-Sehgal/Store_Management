-- I am assuming here that if Inventory level < Demand Forecast, then the product might soon go out of stock.

-- Getting the Latest Inventory + Forecast per Product
SELECT 
    I.Store_ID,
    I.Region,
    I.Product_ID,
    P.Category,
    I.Inventory_Level,
    F.Demand_Forecast,
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
JOIN Forecast F
    ON I.Store_ID = F.Store_ID
    AND I.Region = F.Region
    AND I.Product_ID = F.Product_ID
    AND I.Date = F.Date
JOIN Product P 
    ON I.Product_ID = P.Product_ID
WHERE I.Inventory_Level < F.Demand_Forecast;
