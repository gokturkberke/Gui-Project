from models.transaction import Transaction
import sqlite3
from viewmodels.settings_viewmodel import I18N

class FinancialGoalViewModel:
    def __init__(self):
        self.financial_goal = ""

    def set_financial_goal(self, goal):
        if goal.isdigit():
            self.financial_goal = goal
            return True
        else:
            return False

    def get_financial_goal(self):
        return self.financial_goal