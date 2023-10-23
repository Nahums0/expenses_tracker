# connection.py

import os
import psycopg2
from contextlib import contextmanager

# Connection pool
connection_pool = []

def get_db_connection_parameters():
    #TODO: Remove defaults
    return {
        "database": os.environ.get("DB_NAME", "postgres"),
        "user": os.environ.get("DB_USER", "omer"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": os.environ.get("DB_PORT", "5432"),
    }

@contextmanager
def get_connection():
    if not connection_pool:
        connection_pool.append(psycopg2.connect(**get_db_connection_parameters()))
    connection = connection_pool.pop()
    try:
        yield connection
    finally:
        connection_pool.append(connection)

def close_connection(connection):
    connection.close()

def execute_query(connection, query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        
        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
            return results
        else:
            connection.commit()

@contextmanager
def transaction(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor

def close_connections():
    for connection in connection_pool:
        connection.close()
