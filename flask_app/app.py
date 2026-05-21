from flask import Flask, render_template, request, session
import pickle
import pandas as pd
import os
# from src.db import get_connection
from flask_app.admin.routes import admin

# ✅ CREATE APP FIRST
app = Flask(__name__)

# ✅ CONFIG AFTER CREATION
app.secret_key = "secret123"

# ✅ REGISTER BLUEPRINT
app.register_blueprint(admin)

# ✅ GET PROJECT ROOT
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ✅ MODEL PATH
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# ✅ LOAD MODEL
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# ✅ HELPER FUNCTION
def convert(x):
    return 1 if x == "yes" else 0

# ✅ HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")

# ✅ PREDICTION ROUTE
@app.route("/predict", methods=["POST"])
def predict():
    name = request.form["name"]
    age = int(request.form["age"])

    fever = convert(request.form["fever"])
    cough = convert(request.form["cough"])
    headache = convert(request.form["headache"])
    fatigue = convert(request.form["fatigue"])

    # ✅ DataFrame input
    input_data = pd.DataFrame(
        [[age, fever, cough, headache, fatigue]],
        columns=['age', 'fever', 'cough', 'headache', 'fatigue']
    )

    prediction = model.predict(input_data)[0]

    # ✅ Risk logic
    risk = "HIGH" if prediction in ["Critical Infection", "Viral Infection"] else "LOW"

    return render_template(
        "result.html",
        name=name,
        prediction=prediction,
        risk=risk
    )

# ✅ RUN SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)