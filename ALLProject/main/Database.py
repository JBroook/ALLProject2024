import sqlite3 as sql

import bcrypt

conn = sql.connect("DriveEase.db")
cursor = conn.cursor()

#user stuff
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS USERS (
        USER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        USERNAME VARCHAR(255) NOT NULL,
        EMAIL VARCHAR(255) NOT NULL,
        USER_PASSWORD VARCHAR(255) NOT NULL,
        FIRST_NAME VARCHAR(255) NOT NULL,
        LAST_NAME VARCHAR(255) NOT NULL,
        DATE_OF_BIRTH VARCHAR(100) NOT NULL,
        CONTACT_NUMBER VARCHAR(255) NOT NULL,
        IC_NUMBER VARCHAR(15) NOT NULL
    )
    '''
)

conn.commit()

#check if admin account exists, if no, create one
cursor.execute("SELECT * FROM USERS WHERE USERNAME = 'Admin';")
result = cursor.fetchall()
if len(result)==0:
    admin_password = bcrypt.hashpw("Admin@1234".encode(), bcrypt.gensalt())
    cursor.execute('''
    INSERT INTO USERS (USERNAME, EMAIL, USER_PASSWORD, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, CONTACT_NUMBER, IC_NUMBER)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ("Admin","driveease3@gmail.com",admin_password,"Admin","Account","2000-01-01","",""))

conn.commit()

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
        "plate_number" : "PPZ 1023",

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
        RATING_DATE VARCHAR(10) NOT NULL,
        FOREIGN KEY (BOOKING_ID) REFERENCES BOOKINGS(BOOKING_ID)
    )''')
conn.commit()

#payment stuff
cursor.execute('''CREATE TABLE IF NOT EXISTS PAYMENTS (
        PAYMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NAME VARCHAR(255) NOT NULL,
        CARD_NUMBER VARCHAR(255) NOT NULL,
        EXPIRY VARCHAR(255) NOT NULL,
        CVC VARCHAR(255) NOT NULL,
        BOOKING_ID INTEGER NOT NULL,
        DATE_PAID VARCHAR(10) NOT NULL,
        FOREIGN KEY (BOOKING_ID) REFERENCES BOOKINGS(BOOKING_ID)
    )''')
conn.commit()