import mysql.connector

# دالة لجلب صفحة واحدة من قاعدة البيانات باستخدام LIMIT و OFFSET
def paginate_users(page_size, offset):
    # الاتصال بقاعدة بيانات ALX_prodev
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",       # ← غيّرها حسب إعدادات MySQL عندك
        password="your_password",   # ← غيّرها حسب إعدادات MySQL عندك
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    # جلب البيانات باستخدام LIMIT و OFFSET
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

# دالة Generator ترجع الصفحات واحدة واحدة (كل صفحة عند الطلب = Lazy)
def lazy_pagination(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break  # لما تخلص الصفوف في الجدول
        yield page
        offset += page_size
