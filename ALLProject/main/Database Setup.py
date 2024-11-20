import sqlite3 as sql
import bcrypt

conn = sql.connect("DriveEase.db")
cursor = conn.cursor()

cursor.execute(
    '''
    INSERT INTO USERS (USERNAME, EMAIL, USER_PASSWORD, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, CONTACT_NUMBER, IC_NUMBER)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?) 
    ''',
    (
        "ParkKimJun",
        "jeremiahboey3@gmail.com",
        bcrypt.hashpw("Lettuce123".encode(),bcrypt.gensalt()),
        "Park",
        "Kim",
        "2000-01-01",
        "60132433391",
        "012345678912"
    )
)

conn.commit()

cursor.execute(
    '''
    INSERT INTO USERS (USERNAME, EMAIL, USER_PASSWORD, FIRST_NAME, LAST_NAME, DATE_OF_BIRTH, CONTACT_NUMBER, IC_NUMBER)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?) 
    ''',
    (
        "KamalaHarris",
        "kamalaharris@gmail.com",
        bcrypt.hashpw("Lettuce123".encode(),bcrypt.gensalt()),
        "Kamala",
        "Harris",
        "1998-11-25",
        "60162443324",
        "013454474913"
    )
)

conn.commit()

cursor.execute(
    '''
    INSERT INTO BOOKINGS (START_DATE, END_DATE, LOCATION, CAR_ID, USER_ID, CURRENT_BOOKING, STATUS, TOTAL_CHARGE)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?) 
    ''',
    (
        "2023-10-01",
        "2023-10-06",
        "Pantai Jerejak",
        3,
        2,
        0,
        "Paid",
        1050
    )
)

conn.commit()

cursor.execute(
    '''
    INSERT INTO BOOKINGS (START_DATE, END_DATE, LOCATION, CAR_ID, USER_ID, CURRENT_BOOKING, STATUS, TOTAL_CHARGE)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?) 
    ''',
    (
        "2024-11-15",
        "2024-11-18",
        "Pantai Jerejak",
        1,
        2,
        0,
        "Paid",
        1020
    )
)

conn.commit()

cursor.execute(
    '''
    INSERT INTO BOOKINGS (START_DATE, END_DATE, LOCATION, CAR_ID, USER_ID, CURRENT_BOOKING, STATUS, TOTAL_CHARGE)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?) 
    ''',
    (
        "2024-11-30",
        "2024-12-05",
        "Pantai Jerejak",
        5,
        3,
        1,
        "Pending",
        840
    )
)

conn.commit()

cursor.execute(
    '''
    INSERT INTO PAYMENTS (NAME, CARD_NUMBER, EXPIRY, CVC, BOOKING_ID, DATE_PAID)
    VALUES(?, ?, ?, ?, ?, ?) 
    ''',
    (
        "Park Kim Jun",
        "4235 2346 0987 8329",
        "08/28",
        "653",
        1,
        "2024-09-24"
    )
)

conn.commit()

cursor.execute(
    '''
    INSERT INTO PAYMENTS (NAME, CARD_NUMBER, EXPIRY, CVC, BOOKING_ID, DATE_PAID)
    VALUES(?, ?, ?, ?, ?, ?) 
    ''',
    (
        "Park Kim Jun",
        "4235 2346 0987 8329",
        "08/28",
        "653",
        1,
        "2024-06-03"
    )
)

conn.commit()

cursor.execute(
    '''
    INSERT INTO RATINGS (SCORE, REVIEW, BOOKING_ID, RATING_DATE)
    VALUES(?, ?, ?, ?) 
    ''',
    (
        5,
        "Decent ride with friendly customer service. Would use again!",
        1,
        "2023-10-25"
    )
)

conn.commit()