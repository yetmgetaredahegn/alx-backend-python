#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data in batches.
    Each batch is a list of dictionaries (rows).
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="deAlto#Crack357",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        while True:
            batch = cursor.fetchmany(batch_size)  # fetch a chunk of rows
            if not batch:
                break
            yield batch  # yield the batch

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Processes batches of users and prints those over age 25.
    Uses the stream_users_in_batches generator.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1: iterate batches
        for user in batch:                               # loop 2: iterate users in batch
            if user['age'] > 25:                         # filter users over 25
                print(user)
