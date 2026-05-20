from src.db import get_connection

conn = get_connection()
cursor = conn.cursor()

print("=== UPDATE PATIENT ===")

pid = int(input("Enter Patient ID: "))
risk = input("New Risk Level (HIGH/LOW): ")

sql = "UPDATE patients SET risk_level=%s WHERE id=%s"
cursor.execute(sql, (risk, pid))

conn.commit()

print("Patient Updated ✔️")

conn.close()