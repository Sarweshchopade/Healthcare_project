from flask import Flask, request, jsonify
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from flask_cors import CORS  # 🆕 For handling requests from Flutter frontend

app = Flask(__name__)
CORS(app)  # 🆕 Enable CORS for all routes

bcrypt = Bcrypt(app)

# JWT Secret Key
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1212",
    database="healthcare_db"
)
cursor = db.cursor(dictionary=True)

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name, email, password = data["name"], data["email"], data["password"]
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)", 
            (name, email, hashed_password)
        )
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.Error as err:
        print(f"Error: {err}")  # 🆕 Better error logging
        return jsonify({"message": "User already exists or database error"}), 400

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email, password = data["email"], data["password"]

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user["password_hash"], password):
        access_token = create_access_token(identity=user["id"])
        return jsonify({"token": access_token, "user": user}), 200

    return jsonify({"message": "Invalid credentials"}), 401

# Protected Route
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    return jsonify({"message": "Access Granted"}), 200

# Root route (optional)
@app.route('/')
def home():
    return jsonify({"message": "Welcome to Healthcare API!"}), 200

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
