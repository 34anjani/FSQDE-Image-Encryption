import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="fsqdeuser",
        password="fsqde123",
        database="fsqde"
    )
