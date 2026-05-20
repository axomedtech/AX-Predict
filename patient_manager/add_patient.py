from src.db import get_connection

conn = get_connection()
cursor = conn.cursor()

print("=== ADD PATIENT ===")

name = input("Name: ")
age = int(input("Age: "))
fever = int(input("Fever (0/1): "))
cough = int(input("Cough (0/1): "))
headache = int(input("Headache (0/1): "))
fatigue = int(input("Fatigue (0/1): "))
risk = input("Risk Level (HIGH/LOW): ")

sql = """
INSERT INTO patients (name, age, fever, cough, headache, fatigue, risk_level)
VALUES (%s,%s,%s,%s,%s,%s,%s)
"""

cursor.execute(sql, (name, age, fever, cough, headache, fatigue, risk))
conn.commit()

print("Patient Added ✔️")

conn.close()