import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",      # ← غيّر ده باسم المستخدم بتاعك
        password="your_password",  # ← غيّر ده بالباسورد بتاعك
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
