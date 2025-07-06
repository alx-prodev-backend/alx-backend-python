import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator to stream user data in batches"""
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",  # ← غيّر باسم المستخدم
        password="your_password",  # ← غيّر بكلمة السر
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch  # yield any remaining rows

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Processes users in batches, prints users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
