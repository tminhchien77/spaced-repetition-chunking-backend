from psycopg2.pool import SimpleConnectionPool

pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    user="tranminhchien",
    password="tranminhchien",
    host="localhost",
    port=5432,
    database="src_system"
)

def get_connection():
    conn = pool.getconn()
    conn.autocommit = True
    return conn

def close_connection(conn):
    pool.putconn(conn)