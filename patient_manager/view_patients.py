from src.db import get_connection
import pandas as pd

conn = get_connection()

df = pd.read_sql("SELECT * FROM patients", conn)

print("===== PATIENT LIST =====")
print(df)

conn.close()