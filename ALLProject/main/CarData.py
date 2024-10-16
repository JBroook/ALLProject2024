import sqlite3 as sql

conn = sql.connect("DriveEase.db")
cursor = conn.cursor()

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS CARS 
    (
        CAR_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        MANUFACTURER_YEAR INTEGER NOT NULL,
        MODEL VARCHAR(255) NOT NULL,
        PRICE INTEGER NOT NULL,
        IMAGE VARCHAR(255) NOT NULL
    )
    '''
)

car_list = [
    {
        "manufacturer_year" : 2010,
        "model" : "Honda Accord",
        "price" : 255,
        "image" : "honda accord.png"
    },

    {
        "manufacturer_year" : 2013,
        "model" : "Honda City",
        "price" : 180,
        "image" : "honda city.png"
    },

    {
        "manufacturer_year" : 2012,
        "model" : "Honda Civic",
        "price" : 150,
        "image" : "honda civic.png"
    },
    {
        "manufacturer_year" : 2022,
        "model" : "Hyundai Sonata",
        "price" : 200,
        "image" : "hyundai sonata.png"
    },
    {
        "manufacturer_year" : 2018,
        "model" : "Nissan Serena",
        "price" : 140,
        "image" : "nissan serena.png"
    },
    {
        "manufacturer_year" : 2012,
        "model" : "Perodua Myvi",
        "price" : 100,
        "image" : "perodua myvi.png"
    }
]

cursor.execute("SELECT * FROM CARS")
result = cursor.fetchall()

if len(result)==0:
    for car in car_list:
        query = f'''
        INSERT INTO CARS
        (
            MANUFACTURER_YEAR, 
            MODEL, 
            PRICE, 
            IMAGE
        )
        VALUES
        (
            {car["manufacturer_year"]},
            \'{car["model"]}\',
            {car["price"]},
            \'{car["image"]}\'
        )
        '''
        cursor.execute(query)

    conn.commit()