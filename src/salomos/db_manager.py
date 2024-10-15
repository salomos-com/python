import sqlite3
from typing import Dict, Any

class DBManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.init_database()

    def init_database(self):
        # Create sentences table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentence TEXT NOT NULL,
            processed BOOLEAN DEFAULT 0
        )
        ''')

        # Create objects table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value TEXT NOT NULL
        )
        ''')

        self.conn.commit()

    def load_sentence(self) -> str:
        self.cursor.execute("SELECT id, sentence FROM sentences WHERE processed = 0 LIMIT 1")
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute("UPDATE sentences SET processed = 1 WHERE id = ?", (result[0],))
            self.conn.commit()
            return result[1]
        return ""

    def load_objects(self) -> Dict[str, Any]:
        self.cursor.execute("SELECT name, value FROM objects")
        return {row[0]: eval(row[1]) for row in self.cursor.fetchall()}

    def close(self):
        self.conn.close()
