import sqlite3
import functools
from datetime import datetime  # ✅ Added as requested

# Decorator to log SQL queries with timestamps
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get query from args or kwargs
        query = kwargs.get('query')
        if not query and args:
            query = args[0]

        if query:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Executing SQL query: {query}")
        else:
            print("[LOG] No SQL query found to log.")

        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
users = fetch_all_users(query="SELECT * FROM users")
