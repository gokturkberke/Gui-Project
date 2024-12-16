from models.transaction import Transaction
import sqlite3
from viewmodels.settings_viewmodel import I18N
from viewmodels.financial_goal_viewmodel import FinancialGoalViewModel

DB_NAME = "finance_manager.db"

class MainViewModel:
    def __init__(self, language_code="en"):
        self.language = language_code
        self.i18n = I18N(self.language)
        self.financial_goal_viewmodel = FinancialGoalViewModel()

    def set_language(self, lang):
        self.language = lang
        self.i18n = I18N(lang)

    def get_translation(self, key, **kwargs):
        translation = self.i18n.translations.get(key, key)
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
        cursor.execute("SELECT id, date, type, amount, category FROM transactions")
        rows = cursor.fetchall()
        conn.close()
        transactions = [Transaction(row[2], row[4], row[3], row[1], row[0]) for row in rows]
        return transactions

    def delete_transaction(self, transaction_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        conn.close()

    def update_transaction(self, transaction_id, transaction_type, category, amount, date):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE transactions
            SET type = ?, category = ?, amount = ?, date = ?
            WHERE id = ?
        """, (transaction_type, category, amount, date, transaction_id))
        conn.commit()
        conn.close()

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
    
    def set_financial_goal(self, expense_limit, income_goal):
        return self.financial_goal_viewmodel.set_financial_goal(expense_limit, income_goal)

    def get_financial_goal(self):
        return self.financial_goal_viewmodel.get_financial_goal()

    def get_actual_expense(self, start_date=None, end_date=None):
        return self.financial_goal_viewmodel.get_actual_expense(start_date, end_date)

    def get_actual_income(self, start_date=None, end_date=None):
        return self.financial_goal_viewmodel.get_actual_income(start_date, end_date)

    def translate_category(self, category):
        return self.get_translation(category)