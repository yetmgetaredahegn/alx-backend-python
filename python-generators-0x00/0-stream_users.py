#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that streams rows from user_data table one by one"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="deAlto#Crack357",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)  # dictionary=True gives column names

        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row   # yield one row at a time

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
