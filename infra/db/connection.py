# from psycopg2.pool import SimpleConnectionPool

# pool = SimpleConnectionPool(
#     minconn=1,
#     maxconn=10,
#     user="tranminhchien",
#     password="tranminhchien",
#     host="localhost",
#     port=5432,
#     database="src_system"
# )

# def get_connection():
#     conn = pool.getconn()
#     conn.autocommit = True
#     return conn

# def close_connection(conn):
#     pool.putconn(conn)

import os
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ENV = os.getenv("ENV", "local")

sslmode = "require" if ENV == "production" else "disable"

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DATABASE_URL,
    sslmode=sslmode
)

def get_connection():
    conn = pool.getconn()
    conn.autocommit = True
    return conn

def close_connection(conn):
    pool.putconn(conn)
