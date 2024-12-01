from models.transaction import Transaction
import sqlite3

DB_NAME = "finance_manager.db"

class MainViewModel:
    def __init__(self):
        self.language = "en"

    def set_language(self, lang):
        self.language = lang

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