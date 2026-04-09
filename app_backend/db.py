import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="alumno",
        password="alumno123",
        database="prode"
    )