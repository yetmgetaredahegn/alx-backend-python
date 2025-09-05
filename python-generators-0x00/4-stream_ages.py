#!/usr/bin/python3
import seed  # your seed.py module

def stream_user_ages():
    """Generator that lazily yields user ages one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:  # loop #1
        yield row['age']
    
    cursor.close()
    connection.close()


def calculate_average_age():
    """Calculates average age using the generator."""
    total = 0
    count = 0
    
    for age in stream_user_ages():  # loop #2
        total += age
        count += 1
    
    if count == 0:
        return 0
    return total / count


if __name__ == "__main__":
    avg_age = calculate_average_age()
    print(f"Average age of users: {avg_age:.2f}")

