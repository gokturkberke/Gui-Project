import ttkbootstrap as ttk
from tkinter import messagebox
from views.transaction_view import TransactionView
from views.settings_view import SettingsView
from views.transaction_viewer import TransactionViewer
from views.budget_overview import BudgetOverview
from views.financial_goal_view import FinancialGoalView

class MainView(ttk.Window):
    def __init__(self, viewmodel):
        super().__init__(themename="litera")
        self.viewmodel = viewmodel
        self.title(self.get_translation("title"))
        self.geometry("600x400")
        self.init_main_menu()

    def init_main_menu(self):
        self.clear_frame()
        self.label = ttk.Label(self, text=self.get_translation("title"), font=("Arial", 20))
        self.label.pack(pady=20)
        buttons = [
            (self.get_translation("add_income"), self.open_add_income),
            (self.get_translation("add_expense"), self.open_add_expense),
            (self.get_translation("view_transactions"), self.open_view_transactions),
            (self.get_translation("budget_overview"), self.open_budget_overview),
            (self.get_translation("financial_goal"), self.open_financial_goal),
            (self.get_translation("settings"), self.open_settings),
            (self.get_translation("exit"), self.confirm_exit),
        ]
        self.button_widgets = []
        for text, command in buttons:
            button = ttk.Button(self, text=text, width=25, command=command)
            button.pack(pady=5)
            self.button_widgets.append(button)

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
    
    def open_financial_goal(self):
        self.financial_goal_view = FinancialGoalView(self, self.viewmodel)
        
    def open_settings(self):
        SettingsView(self, self.viewmodel)

    def confirm_exit(self):
        if messagebox.askyesno(
            title=self.get_translation("exit_confirmation_title"),
            message=self.get_translation("exit_confirmation_message")
        ):
            self.destroy()

    def get_translation(self, key, **kwargs):
        return self.viewmodel.get_translation(key, **kwargs)

    def refresh_ui(self):
        self.title(self.get_translation("title"))
        self.init_main_menu()
        if hasattr(self, 'transaction_view'):
            self.transaction_view.refresh_ui()
        if hasattr(self, 'transaction_viewer') and self.transaction_viewer:
            #self.transaction_viewer.clear_frame()
            self.transaction_viewer.transactions = self.transaction_viewer.load_transactions()
            self.transaction_viewer.translate_categories()
            self.transaction_viewer.init_ui()
        if hasattr(self, 'budget_overview'):
            self.budget_overview.refresh_ui()