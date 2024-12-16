import ttkbootstrap as ttk
from tkinter import messagebox
from viewmodels.financial_goal_viewmodel import FinancialGoalViewModel
from viewmodels.settings_viewmodel import SettingsViewModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap.widgets import DateEntry

class FinancialGoalView(ttk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.settings_viewmodel = SettingsViewModel(viewmodel.language)
        self.title(self.get_translation("financial_goal"))
        self.geometry("1150x850")
        self.resizable(False, False)
        self.init_ui()

    def get_translation(self, key, **kwargs):
        return self.viewmodel.get_translation(key, **kwargs)

    def submit_goal(self):
        expense_limit = self.expense_limit_entry.get()
        income_goal = self.income_goal_entry.get()
        if self.viewmodel.set_financial_goal(expense_limit, income_goal):
            messagebox.showinfo(
                self.get_translation("success"),
                self.get_translation("success_goal").format(expense_limit=expense_limit, income_goal=income_goal)
            )
        else:
            messagebox.showerror(self.get_translation("error"), self.get_translation("error_goal"))

    def init_ui(self):
        self.expense_limit_label = ttk.Label(self, text=self.get_translation("enter_your_expense_limit"))
        self.expense_limit_label.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        self.expense_limit_entry = ttk.Entry(self)
        self.expense_limit_entry.grid(row=0, column=1, padx=20, pady=20, sticky="w")

        self.income_goal_label = ttk.Label(self, text=self.get_translation("enter_your_income_goal"))
        self.income_goal_label.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        self.income_goal_entry = ttk.Entry(self)
        self.income_goal_entry.grid(row=0, column=3, padx=20, pady=20, sticky="w")

        self.submit_button = ttk.Button(self, text=self.get_translation("save"), command=self.submit_goal)
        self.submit_button.grid(row=0, column=4, columnspan=2, pady=20, padx=20)

        self.show_chart_button = ttk.Button(self, text=self.get_translation("show_chart"), command=self.show_chart)
        self.show_chart_button.grid(row=0, column=6, columnspan=2, pady=20, padx=20)

        self.chart_frame = ttk.Frame(self)
        self.chart_frame.grid(row=2, column=0, columnspan=8, pady=20, padx=20)

        # Date range selection
        self.start_date_label = ttk.Label(self, text=self.get_translation("start_date"))
        self.start_date_label.grid(row=1, column=0, padx=20, pady=20, sticky="e")

        self.start_date_entry = DateEntry(self)
        self.start_date_entry.grid(row=1, column=1, padx=20, pady=20, sticky="w")

        self.end_date_label = ttk.Label(self, text=self.get_translation("end_date"))
        self.end_date_label.grid(row=1, column=2, padx=20, pady=20, sticky="e")

        self.end_date_entry = DateEntry(self)
        self.end_date_entry.grid(row=1, column=3, padx=20, pady=20, sticky="w")

        self.all_time_button = ttk.Button(self, text=self.get_translation("show_all_time"), command=self.show_all_time_chart)
        self.all_time_button.grid(row=1, column=5, padx=20, pady=20, sticky="w")
        
        # Fetch and set the previously submitted financial goals
        expense_limit, income_goal = self.viewmodel.get_financial_goal()
        self.expense_limit_entry.insert(0, expense_limit or "")
        self.income_goal_entry.insert(0, income_goal or "")

    def show_all_time_chart(self):
        # Fetch the financial goals
        expense_limit, income_goal = self.viewmodel.get_financial_goal()

        # Fetch actual expense and income for all available dates
        actual_expense = self.viewmodel.get_actual_expense()
        actual_income = self.viewmodel.get_actual_income()

        # Data for the chart
        labels = [self.get_translation("expense"), self.get_translation("income")]
        goals = [float(expense_limit), float(income_goal)]
        actuals = [actual_expense, actual_income]

        x = range(len(labels))

        # Create a bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars1 = ax.bar(x, goals, width=0.4, label=self.get_translation("goal"), align='center', color='skyblue')
        bars2 = ax.bar(x, actuals, width=0.4, label=self.get_translation("actual"), align='edge', color='lightgreen')

        ax.set_xlabel(self.get_translation("category"))
        ax.set_ylabel(self.get_translation("amount"))
        ax.set_title(self.get_translation("financial_goals_vs_actuals"))
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        # Add data labels on top of the bars
        for bar in bars1:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom')

        for bar in bars2:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom')

        # Clear the previous chart if it exists
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=ttk.BOTH, expand=True)
        
    
    def show_chart(self):
        # Fetch the financial goals
        expense_limit, income_goal = self.viewmodel.get_financial_goal()

        # Retrieve the date range from the DateEntry widgets
        start_date = self.start_date_entry.entry.get()
        end_date = self.end_date_entry.entry.get()

        # Fetch actual expense and income for the given date range
        actual_expense = self.viewmodel.get_actual_expense(start_date, end_date)
        actual_income = self.viewmodel.get_actual_income(start_date, end_date)

        # Data for the chart
        labels = [self.get_translation("expense"), self.get_translation("income")]
        goals = [float(expense_limit), float(income_goal)]
        actuals = [actual_expense, actual_income]

        x = range(len(labels))

        # Create a bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars1 = ax.bar(x, goals, width=0.4, label=self.get_translation("goal"), align='center', color='skyblue')
        bars2 = ax.bar(x, actuals, width=0.4, label=self.get_translation("actual"), align='edge', color='lightgreen')

        ax.set_xlabel(self.get_translation("category"))
        ax.set_ylabel(self.get_translation("amount"))
        ax.set_title(self.get_translation("financial_goals_vs_actuals"))
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        # Add data labels on top of the bars
        for bar in bars1:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom')

        for bar in bars2:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.2f}', va='bottom')

        # Clear the previous chart if it exists
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=ttk.BOTH, expand=True)