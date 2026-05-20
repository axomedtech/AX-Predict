import pickle
from db import get_connection

print("============= AX-Predict =============")

name = input("Enter Name : ")
age = int(input("Enter Age : "))

print("\nEnter Symptoms (yes/no)")

def convert(x):
    return 1 if x.lower() == "yes" else 0

fever = convert(input("Fever : "))
cough = convert(input("Cough : "))
headache = convert(input("Headache : "))
fatigue = convert(input("Fatigue : "))

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Predict
prediction = model.predict([[age, fever, cough, headache, fatigue]])[0]
print("\n=========== RESULT ===========")
print("Name :", name)
print("Predicted Disease :", prediction)

# STORE RESULT IN MYSQL (patients table)
conn = get_connection()
cursor = conn.cursor()

sql = """
INSERT INTO patients (name, age, fever, cough, headache, fatigue, risk_level)
VALUES (%s,%s,%s,%s,%s,%s,%s)
"""

# Risk mapping
risk = "HIGH" if prediction in ["Critical Infection", "Viral Infection"] else "LOW"

cursor.execute(sql, (name, age, fever, cough, headache, fatigue, risk))
conn.commit()
conn.close()

print("Saved to database ✔️")