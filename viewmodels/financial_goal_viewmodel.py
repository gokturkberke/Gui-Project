import sqlite3
from models.database import DB_NAME

class FinancialGoalViewModel:
    def __init__(self, language=None):
        self.db_path = DB_NAME
        self.language = language

    def get_translation(self, key, **kwargs):
        # Placeholder for translation method
        # You might want to implement this based on your translation logic
        return key

    def set_financial_goal(self, expense_limit, income_goal):
        if expense_limit.isdigit() and income_goal.isdigit() and expense_limit and income_goal:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""DELETE FROM financial_goals""")  # Ensures only one goal exists
                cursor.execute(
                    """INSERT INTO financial_goals (expense_limit, income_goal) VALUES (?, ?)""",
                    (expense_limit, income_goal)
                )
                conn.commit()
            return True
        return False

    def get_financial_goal(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT expense_limit, income_goal FROM financial_goals ORDER BY id DESC LIMIT 1""")
            result = cursor.fetchone()
        return result if result else ("", "")

    def get_actual_expense(self, start_date=None, end_date=None):
        # Implement the method to handle date range or fetch all expenses
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if start_date and end_date:
                cursor.execute("""
                SELECT SUM(amount)
                FROM transactions
                WHERE type = 'Expense' AND date BETWEEN ? AND ?
                """, (start_date, end_date))
            else:
                cursor.execute("""
                SELECT SUM(amount)
                FROM transactions
                WHERE type = 'Expense'
                """)
            result = cursor.fetchone()
        return result[0] if result and result[0] is not None else 0

    def get_actual_income(self, start_date=None, end_date=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if start_date and end_date:
                cursor.execute("""
                SELECT SUM(amount)
                FROM transactions
                WHERE type = 'Income' AND date BETWEEN ? AND ?
                """, (start_date, end_date))
            else:
                cursor.execute("""
                SELECT SUM(amount)
                FROM transactions
                WHERE type = 'Income'
                """)
            result = cursor.fetchone()
        return result[0] if result and result[0] is not None else 0