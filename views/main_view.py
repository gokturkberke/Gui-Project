import tkinter as tk
from tkinter import ttk
from views.transaction_view import TransactionView
from views.settings_view import SettingsView

class MainView(tk.Tk):
    def __init__(self, viewmodel):
        super().__init__()
        self.viewmodel = viewmodel
        self.title("Personal Finance Manager")
        self.geometry("600x400")
        self.init_main_menu()

    def init_main_menu(self):
        tk.Label(self, text="Personal Finance Manager", font=("Arial", 20)).pack(pady=20)
        buttons = [
            ("Add Income", self.open_add_income),
            ("Add Expense", self.open_add_expense),
            ("View Transactions", self.open_view_transactions),
            ("Budget Overview", self.open_budget_overview),
            ("Settings", self.open_settings),
        ]
        for text, command in buttons:
            tk.Button(self, text=text, width=25, command=command).pack(pady=5)

    def open_add_income(self):
        TransactionView(self, "Income", self.viewmodel)

    def open_add_expense(self):
        TransactionView(self, "Expense", self.viewmodel)

    def open_view_transactions(self):
        # Implement view transactions logic
        pass

    def open_budget_overview(self):
        # Implement budget overview logic
        pass

    def open_settings(self):
        SettingsView(self, self.viewmodel)