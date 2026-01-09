import sqlite3
from config import DB_PATH, DEFAULT_USD_RATE

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                item TEXT,
                description TEXT,
                amount REAL,
                created_at TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        if self.get_setting("monthly_salary") is None:
            self.update_setting("monthly_salary", 0)

        if self.get_setting("usd_rate") is None:
            self.update_setting("usd_rate", DEFAULT_USD_RATE)

        self.conn.commit()

    # ---------------- EXPENSES ----------------
    def add_expense(self, category, item, description, amount, created_at):
        self.cursor.execute(
            "INSERT INTO expenses VALUES (NULL, ?, ?, ?, ?, ?)",
            (category, item, description, amount, created_at)
        )
        self.conn.commit()

    def get_today_expenses(self):
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute(
            "SELECT * FROM expenses WHERE created_at LIKE ?",
            (f"{today}%",)
        )
        return [dict(r) for r in self.cursor.fetchall()]

    def get_all_expenses(self):
        self.cursor.execute("SELECT * FROM expenses ORDER BY created_at DESC")
        return [dict(r) for r in self.cursor.fetchall()]

    # ---------------- SETTINGS ----------------
    def get_setting(self, key):
        self.cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = self.cursor.fetchone()
        return float(row["value"]) if row else None

    def update_setting(self, key, value):
        self.cursor.execute("""
            INSERT INTO settings (key,value)
            VALUES (?,?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))
        self.conn.commit()

    # ---------------- TOTALS ----------------
    def get_today_total(self):
        return sum(e["amount"] for e in self.get_today_expenses())

    def get_monthly_total(self):
        from datetime import datetime
        month = datetime.now().strftime("%Y-%m")
        self.cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE created_at LIKE ?",
            (f"{month}%",)
        )
        row = self.cursor.fetchone()
        return row[0] if row[0] else 0

    def get_usd_rate(self):
        return self.get_setting("usd_rate") or DEFAULT_USD_RATE

    # ---------------- RESET ----------------
    def reset_all(self):
        self.cursor.execute("DELETE FROM expenses")
        self.cursor.execute("DELETE FROM settings")
        self.conn.commit()
        self.update_setting("monthly_salary", 0)
        self.update_setting("usd_rate", DEFAULT_USD_RATE)
