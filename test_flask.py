import mysql.connector
from mysql.connector import Error

print("🔌 Connecting to MySQL...")

try:
    print("⏳ Trying to connect to 127.0.0.1:3306 with user 'root'")
    conn = mysql.connector.connect(
        host="127.0.0.1",  # Important: use IP instead of 'localhost'
        user="root",
        password="1212",
        database="healthcare_db",
        port=3306,
        connection_timeout=5  # Prevent hanging
    )

    if conn.is_connected():
        print("✅ Connected to MySQL!")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("📋 Tables in healthcare_db:", tables)
        conn.close()
    else:
        print("❌ Connection failed, unknown reason.")

except Error as e:
    print("❌ MySQL Connection Error:", e)
