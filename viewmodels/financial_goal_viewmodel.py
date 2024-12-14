import sqlite3
from viewmodels.settings_viewmodel import I18N
from models.database import DB_NAME

class FinancialGoalViewModel:
    def __init__(self):
        self.db_path = DB_NAME

    def set_financial_goal(self, expense_limit, income_goal):
        if expense_limit.isdigit() and income_goal.isdigit():
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM financial_goals')
                cursor.execute('INSERT INTO financial_goals (expense_limit, income_goal) VALUES (?, ?)', (expense_limit, income_goal))
                conn.commit()
            return True
        else:
            return False

    def get_financial_goal(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT expense_limit, income_goal FROM financial_goals ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            return result if result else ("", "")

    def get_actual_expense(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(amount) FROM transactions WHERE type = "expense"')
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0

    def get_actual_income(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(amount) FROM transactions WHERE type = "income"')
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0