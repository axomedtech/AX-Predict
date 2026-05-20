from src.db import get_connection

conn = get_connection()
cursor = conn.cursor()

print("=== DELETE PATIENT ===")

pid = int(input("Enter Patient ID: "))

sql = "DELETE FROM patients WHERE id=%s"
cursor.execute(sql, (pid,))

conn.commit()

print("Patient Deleted ✔️")

conn.close()