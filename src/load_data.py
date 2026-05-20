import pandas as pd
from db import get_connection

def load_ml_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM ml_data", conn)
    conn.close()
    return df