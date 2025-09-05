import mysql.connector
from mysql.connector import Error
import uuid
import csv

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",   
            user="root",        
            password="deAlto#Crack357" 
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="deAlto#Crack357",
            database="ALX_prodev"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, data_file):
    cursor = connection.cursor()
    with open(data_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row["name"]
            email = row["email"]
            age = row["age"]

            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, age))
    connection.commit()
    cursor.close()

