import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aravindhan@2011",
        database="ax_health"
    )