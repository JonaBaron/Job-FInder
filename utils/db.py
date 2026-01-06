from sqlite3 import Connection, connect
from models.job import job, status
DB_NAME = "jobs.db"
def get_db_connection() -> Connection:
    conn = connect(DB_NAME)
    conn.row_factory = lambda cursor, row: job(
        id=row[0],
        title=row[1],
        company=row[2],
        location=row[3],
        link=row[4],
        status=row[5]
    )
    return conn
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            link TEXT NOT NULL,
            status INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()