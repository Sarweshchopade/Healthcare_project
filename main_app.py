print(">>> main_app.py loaded - starting debug log")

# Importing modules
print(">>> Importing Flask...")
from flask import Flask, request, jsonify

print(">>> Importing MySQL Connector...")
import mysql.connector

print(">>> Importing JWT...")
import jwt

print(">>> Importing datetime...")
import datetime

print(">>> Importing bcrypt...")
import bcrypt

print(">>> Importing requests...")
import requests

print(">>> Importing Flask-CORS...")
from flask_cors import CORS

# Create app
print(">>> Creating Flask app...")
app = Flask(__name__)
CORS(app)

# Secret key
app.config['SECRET_KEY'] = 'e7d9c69b99f847179da0e408f9c5b7be63f230abc679d9ecf0ed3ad9a0b40c5c'

# MySQL Database connection
print("🔍 Attempting to connect to MySQL...")
try:
    print("⏳ Connecting to MySQL database...")
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1212",
        database="healthcare_db"
    )
    cursor = db.cursor()
    print("✅ MySQL connected successfully.")
except mysql.connector.Error as err:
    print("❌ Failed to connect to MySQL:", err)

# JWT Token Generator
def generate_token(user_id):
    token = jwt.encode(
        {'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    return token

# =================== ROUTES =================== #

# Home Route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to Healthcare API!"})

# Register
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        return jsonify({"message": "User already exists"}), 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
    db.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    cursor.execute("SELECT id, password FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        token = generate_token(user[0])
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Symptom Checker
@app.route('/check_symptoms', methods=['POST'])
def check_symptoms():
    symptoms = request.json.get('symptoms', [])
    diseases = {
        "fever": "Flu or Infection",
        "cough": "Cold or COVID-19",
        "headache": "Migraine or Dehydration",
        "stomach pain": "Gastric issues or Ulcers"
    }

    result = [diseases.get(sym.lower(), "Unknown") for sym in symptoms]
    return jsonify({"possible_diseases": result})

# Doctor Locator
@app.route('/doctor_locator', methods=['GET'])
def doctor_locator():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"message": "Latitude and longitude required"}), 400

    hospitals = [
        {"name": "City Hospital", "lat": float(lat) + 0.01, "lon": float(lon) + 0.01},
        {"name": "HealthCare Center", "lat": float(lat) - 0.01, "lon": float(lon) - 0.01},
    ]
    return jsonify({"hospitals": hospitals})

# Run App
if __name__ == "__main__":
    try:
        print("🚀 Starting Flask app on http://0.0.0.0:5050")
        app.run(host="0.0.0.0", port=5050, debug=True)
    except Exception as e:
        print("❌ Flask Error:", e)
