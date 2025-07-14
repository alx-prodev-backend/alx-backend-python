import sqlite3
import functools


# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if a 'query' keyword argument exists
        query = kwargs.get('query', None)
        if not query and len(args) > 0:
            query = args[0]  # Assume first positional arg is the query

        if query:
            print(f"[LOG] Executing SQL query: {query}")
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


# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
