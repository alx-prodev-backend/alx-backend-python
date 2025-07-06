import mysql.connector
import csv
import uuid

def connect_db():
    """Connects to MySQL server (no database yet)"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # ← غيرها باسم المستخدم بتاعك
            password="your_password"  # ← غيرها بالباسورد بتاعك
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates ALX_prodev database if it doesn't exist"""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    """Connects directly to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # ← غيرها باسم المستخدم بتاعك
            password="your_password",  # ← غيرها بالباسورد بتاعك
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Creates user_data table if it doesn't exist"""
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    )
    """
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

def insert_data(connection, csv_filename):
    """Inserts data into user_data table from CSV"""
    cursor = connection.cursor()

    with open(csv_filename, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if entry already exists by email
            cursor.execute("SELECT COUNT(*) FROM user_data WHERE email = %s", (row['email'],))
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (
                    str(uuid.uuid4()),
                    row['name'],
                    row['email'],
                    row['age']
                ))
    connection.commit()
    cursor.close()
