import sqlite3 as sql


conn = sql.connect("DriveEase.db")
cursor = conn.cursor()

#car stuff
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS CARS 
    (
        CAR_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        MANUFACTURER_YEAR INTEGER NOT NULL,
        MODEL VARCHAR(255) NOT NULL,
        PRICE INTEGER NOT NULL,
        IMAGE VARCHAR(255) NOT NULL,
        CAPACITY INTEGER NOT NULL,
        RATING INTEGER,
        TRANSMISSION VARCHAR(255) NOT NULL,
        PLATE_NUMBER VARCHAR(10) NOT NULL
    )
    '''
)
conn.commit()

car_list = [
    {
        "manufacturer_year" : 2010,
        "model" : "Honda Accord",
        "price" : 255,
        "image" : "honda accord.png",
        "capacity" : 5,
        "rating" : 4.5,
        "transmission" : "Auto",
        "plate_number" : "PPZ 1023"
    },

    {
        "manufacturer_year" : 2013,
        "model" : "Honda City",
        "price" : 180,
        "image" : "honda city.png",
        "capacity" : 5,
        "rating" : 4.8,
        "transmission" : "Auto",
        "plate_number" : "PJK 4688"
    },

    {
        "manufacturer_year" : 2012,
        "model" : "Honda Civic",
        "price" : 150,
        "image" : "honda civic.png",
        "capacity" : 5,
        "rating" : 3.9,
        "transmission" : "Manual",
        "plate_number" : "PVG 4547"
    },
    {
        "manufacturer_year" : 2022,
        "model" : "Hyundai Sonata",
        "price" : 200,
        "image" : "hyundai sonata.png",
        "capacity" : 5,
        "rating" : 4.2,
        "transmission" : "Manual",
        "plate_number" : "PMS 1851"
    },
    {
        "manufacturer_year" : 2018,
        "model" : "Nissan Serena",
        "price" : 140,
        "image" : "nissan serena.png",
        "capacity" : 7,
        "rating" : 4.9,
        "transmission" : "Auto",
        "plate_number" : "PLP 4158"
    },
    {
        "manufacturer_year" : 2012,
        "model" : "Perodua Myvi",
        "price" : 100,
        "image" : "perodua myvi.png",
        "capacity" : 5,
        "rating" : 4.8,
        "transmission" : "Auto",
        "plate_number" : "PQH 8971"
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
            IMAGE,
            CAPACITY,
            RATING,
            TRANSMISSION,
            PLATE_NUMBER
        )
        VALUES
        (
            {car["manufacturer_year"]},
            \'{car["model"]}\',
            {car["price"]},
            \'{car["image"]}\',
            {car["capacity"]},
            {car["rating"]},
            \'{car["transmission"]}\',
            \'{car["plate_number"]}\'
        )
        '''
        cursor.execute(query)

    conn.commit()


#bookings stuff
cursor.execute('''CREATE TABLE IF NOT EXISTS BOOKINGS (
        BOOKING_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        START_DATE VARCHAR(10) NOT NULL,
        END_DATE VARCHAR(10) NOT NULL,
        LOCATION VARCHAR(255) NOT NULL,
        CAR_ID INTEGER NOT NULL,
        USER_ID INTEGER NOT NULL,
        CURRENT_BOOKING INTEGER NOT NULL,
        STATUS VARCHAR(50) NOT NULL,
        TOTAL_CHARGE INTEGER NOT NULL,
        FOREIGN KEY (CAR_ID) REFERENCES CARS(CAR_ID),
        FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID)
    )''')
conn.commit()

#ratings stuff
cursor.execute('''CREATE TABLE IF NOT EXISTS RATINGS (
        RATING_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        SCORE INTEGER NOT NULL,
        REVIEW TEXT,
        BOOKING_ID INTEGER NOT NULL,
        FOREIGN KEY (BOOKING_ID) REFERENCES BOOKINGS(BOOKING_ID)
    )''')
conn.commit()

#payment stuff
cursor.execute('''CREATE TABLE IF NOT EXISTS PAYMENTS (
        PAYMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NAME VARCHAR(255) NOT NULL,
        CARD_NUMBER VARCHAR(12) NOT NULL,
        EXPIRY VARCHAR(4) NOT NULL,
        CVC INTEGER NOT NULL,
        BOOKING_ID INTEGER NOT NULL,
        FOREIGN KEY (BOOKING_ID) REFERENCES BOOKINGS(BOOKING_ID)
    )''')
conn.commit()