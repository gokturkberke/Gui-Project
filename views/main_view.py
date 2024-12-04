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
        transactions_window = tk.Toplevel(self)
        transactions_window.title("View Transactions")
        transactions_window.geometry("600x400")

        transactions = self.viewmodel.get_transactions()

        tree = ttk.Treeview(transactions_window, columns=("Date", "Type", "Amount", "Description"), show='headings')
        tree.heading("Date", text="Date")
        tree.heading("Type", text="Type")
        tree.heading("Amount", text="Amount")
        tree.heading("Description", text="Description")

        for transaction in transactions:
            tree.insert("", "end", values=(transaction.date, transaction.type, transaction.amount, transaction.description))

        tree.pack(expand=True, fill='both')

    def open_budget_overview(self):
        budget_window = tk.Toplevel(self)
        budget_window.title("Budget Overview")
        budget_window.geometry("600x400")

        budget_data = self.viewmodel.get_budget_overview()

        tree = ttk.Treeview(budget_window, columns=("Category", "Allocated", "Spent", "Remaining"), show='headings')
        tree.heading("Category", text="Category")
        tree.heading("Allocated", text="Allocated")
        tree.heading("Spent", text="Spent")
        tree.heading("Remaining", text="Remaining")

        for category, data in budget_data.items():
            tree.insert("", "end", values=(category, data['allocated'], data['spent'], data['remaining']))

        tree.pack(expand=True, fill='both')

    def open_settings(self):
        SettingsView(self, self.viewmodel)