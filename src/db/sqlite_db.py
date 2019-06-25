import sqlite3


class SqliteDatabase:
    def __init__(self, db_path):
        self._conn = sqlite3.connect(db_path)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing Database...")
        self._conn.commit()
        self._cursor.close()
        self._conn.close()

    def execute(self, sql, params=None):
        self._cursor.execute(sql, params or ())

    def fetch_all(self):
        return self._cursor.fetchall()

    def fetch_one(self):
        return self._cursor.fetchone()

    def query(self, sql, params=None):
        self._cursor.execute(sql, params or ())
        return self._cursor.fetchall()
