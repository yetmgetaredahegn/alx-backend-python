#!/usr/bin/python3
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print(f"[CACHE MISS] Query executed and cached: {query}")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call -> executes and caches
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call -> returns cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)

