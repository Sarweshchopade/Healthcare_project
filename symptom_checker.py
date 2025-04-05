from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load Symptom Dataset
data = pd.read_csv("symptom_data.csv")  # Dataset containing symptoms and diseases

# Prepare the data
X = data.drop(columns=["Disease"])
y = data["Disease"]

# Train a simple Decision Tree Model
model = DecisionTreeClassifier()
model.fit(X, y)

@app.route('/predict_disease', methods=['POST'])
def predict_disease():
    symptoms = request.json.get('symptoms', [])

    # Convert symptoms to binary input
    symptom_input = [1 if symptom in symptoms else 0 for symptom in X.columns]
    
    # Predict Disease
    predicted_disease = model.predict([symptom_input])[0]

    return jsonify({"status": "success", "predicted_disease": predicted_disease})

if __name__ == '__main__':
    app.run(debug=True)
