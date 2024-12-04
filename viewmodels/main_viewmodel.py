from models.transaction import Transaction
import sqlite3
from viewmodels.settings_viewmodel import TRANSLATIONS

DB_NAME = "finance_manager.db"

class MainViewModel:
    def __init__(self):
        self.language = "en"

    def set_language(self, lang):
        self.language = lang

    def get_translation(self, key, **kwargs):
        translation = TRANSLATIONS.get(self.language, {}).get(key, key)
        try:
            return translation.format(**kwargs)
        except KeyError:
            return translation

    def save_transaction(self, transaction_type, category, amount, date):
        transaction = Transaction(transaction_type, category, amount, date)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (type, category, amount, date)
            VALUES (?, ?, ?, ?)
        """, (transaction.type, transaction.category, transaction.amount, transaction.date))
        conn.commit()
        conn.close()

    def get_transactions(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT date, type, amount, category FROM transactions")
        rows = cursor.fetchall()
        conn.close()
        transactions = [Transaction(row[1], row[3], row[2], row[0]) for row in rows]
        return transactions

    def get_budget_overview(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount) as spent
            FROM transactions
            WHERE type = 'Expense'
            GROUP BY category
        """)
        rows = cursor.fetchall()
        conn.close()
        budget_data = {row[0]: {'allocated': 0, 'spent': row[1], 'remaining': 0} for row in rows}
        return budget_data