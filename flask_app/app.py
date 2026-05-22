# =========================
# AXOMED APP.PY
# CLEAN + SAFE + ANALYSIS FIXED
# =========================

from flask import Flask, render_template, request
import pickle
import pandas as pd
from src.db import get_connection
from flask_app.admin.routes import admin

# =========================
# APP SETUP
# =========================

app = Flask(__name__)
app.secret_key = "secret123"
app.register_blueprint(admin)

# =========================
# LOAD MODEL
# =========================

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# =========================
# HELPER
# =========================

def convert(x):
    return 1 if x == "yes" else 0


def get_analysis(age, fever, cough, headache, fatigue):

    symptoms = []

    if fever:
        symptoms.append("Fever")
    if cough:
        symptoms.append("Cough")
    if headache:
        symptoms.append("Headache")
    if fatigue:
        symptoms.append("Fatigue")

    count = len(symptoms)

    if count >= 4:
        analysis = "Severe infection signs detected. Immediate medical attention recommended."
    elif count == 3:
        analysis = "Moderate infection symptoms detected. Monitor carefully."
    elif count == 2:
        analysis = "Mild symptoms detected. Rest and hydration recommended."
    elif count == 1:
        analysis = "Very mild symptoms detected."
    else:
        analysis = "No significant symptoms detected."

    if age >= 60:
        analysis += " High age risk factor present."
    elif age <= 10:
        analysis += " Child patient requires monitoring."

    return analysis


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# PREDICTION
# =========================

@app.route("/predict", methods=["POST"])
def predict():

    name = request.form.get("name", "Unknown")
    age = int(request.form.get("age", 0))

    fever = convert(request.form.get("fever", "no"))
    cough = convert(request.form.get("cough", "no"))
    headache = convert(request.form.get("headache", "no"))
    fatigue = convert(request.form.get("fatigue", "no"))

    input_data = pd.DataFrame(
        [[age, fever, cough, headache, fatigue]],
        columns=["age", "fever", "cough", "headache", "fatigue"]
    )

    prediction = str(model.predict(input_data)[0])

    # =========================
    # FIXED RISK LOGIC
    # =========================

    if "critical" in prediction.lower():
        risk = "HIGH"
    elif "viral" in prediction.lower():
        risk = "MEDIUM"
    else:
        risk = "LOW"

    risk = risk.upper()

    # =========================
    # ANALYSIS
    # =========================

    analysis = get_analysis(age, fever, cough, headache, fatigue)

    # =========================
    # DB SAVE (FIXED ❗ IMPORTANT)
    # =========================

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patients
        (name, age, fever, cough, headache, fatigue, risk_level, prediction)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        name,
        age,
        fever,
        cough,
        headache,
        fatigue,
        risk,
        prediction   # ✅ FIX: NOW SAVING PREDICTION
    ))

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        name=name,
        prediction=prediction,
        risk=risk,
        analysis=analysis
    )


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":
    app.run(debug=True)