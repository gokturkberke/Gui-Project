import tkinter as tk
from tkinter import ttk
from views.transaction_view import TransactionView
from views.settings_view import SettingsView
from views.transaction_viewer import TransactionViewer
from views.budget_overview import BudgetOverview

class MainView(tk.Tk):
    def __init__(self, viewmodel):
        super().__init__()
        self.viewmodel = viewmodel
        self.title(self.get_translation("title"))
        self.geometry("600x400")
        self.init_main_menu()

    def init_main_menu(self):
        self.clear_frame()
        self.label = tk.Label(self, text=self.get_translation("title"), font=("Arial", 20))
        self.label.pack(pady=20)
        buttons = [
            (self.get_translation("add_income"), self.open_add_income),
            (self.get_translation("add_expense"), self.open_add_expense),
            (self.get_translation("view_transactions"), self.open_view_transactions),
            (self.get_translation("budget_overview"), self.open_budget_overview),
            (self.get_translation("settings"), self.open_settings),
        ]
        self.button_widgets = []
        for text, command in buttons:
            button = tk.Button(self, text=text, width=25, command=command)
            button.pack(pady=5)
            self.button_widgets.append(button)

        exit_button = tk.Button(self, text=self.get_translation("exit"), width=25, command=self.exit_app)
        exit_button.pack(pady=5)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def open_add_income(self):
        self.transaction_view = TransactionView(self, "Income", self.viewmodel)

    def open_add_expense(self):
        self.transaction_view = TransactionView(self, "Expense", self.viewmodel)

    def open_view_transactions(self):
        self.transaction_viewer = TransactionViewer(self, self.viewmodel)

    def open_budget_overview(self):
        self.budget_overview = BudgetOverview(self, self.viewmodel)

    def open_settings(self):
        SettingsView(self, self.viewmodel)

    def get_translation(self, key, **kwargs):
        return self.viewmodel.get_translation(key, **kwargs)

    def exit_app(self):
        self.destroy()

    def refresh_ui(self):
        self.title(self.get_translation("title"))
        self.init_main_menu()
        if hasattr(self, 'transaction_view'):
            self.transaction_view.refresh_ui()
        if hasattr(self, 'transaction_viewer'):
            self.transaction_viewer.refresh_ui()
        if hasattr(self, 'budget_overview'):
            self.budget_overview.refresh_ui()