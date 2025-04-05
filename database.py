import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1212",
    database="healthcare_db"
)

cursor = db.cursor()
