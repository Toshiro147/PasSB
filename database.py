import sqlite3
import os

class Database:
    def __init__(self, db_path="vault_data/vault.db"):
        self.db_path = db_path
        # Klasör yoksa oluştur
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    window_title TEXT
                )
            """)
            conn.commit()

    def add_entry(self, app, user, pwd, title):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO passwords (app_name, username, password, window_title) VALUES (?, ?, ?, ?)",
                          (app, user, pwd, title))
            conn.commit()

    def get_all_entries(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM passwords")
            return cursor.fetchall()