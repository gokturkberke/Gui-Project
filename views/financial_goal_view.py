import ttkbootstrap as ttk
from tkinter import messagebox
from viewmodels.financial_goal_viewmodel import FinancialGoalViewModel
from viewmodels.settings_viewmodel import SettingsViewModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FinancialGoalView(ttk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.settings_viewmodel = SettingsViewModel(viewmodel.language)
        self.title(self.get_translation("financial_goal"))
        self.geometry("1300x850")
        self.init_ui()

    def get_translation(self, key, **kwargs):
        return self.viewmodel.get_translation(key, **kwargs)

    def submit_goal(self):
        expense_limit = self.expense_limit_entry.get()
        income_goal = self.income_goal_entry.get()
        if self.viewmodel.set_financial_goal(expense_limit, income_goal):
            messagebox.showinfo("Success", f"Your financial goals have been set!\nExpense Limit: ${expense_limit}\nIncome Goal: ${income_goal}")
        else:
            messagebox.showerror("Error", "Please enter valid numbers for both fields.")
        
    def init_ui(self):
        self.expense_limit_label = ttk.Label(self, text=self.get_translation("enter_your_expense_limit"))
        self.expense_limit_label.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        self.expense_limit_entry = ttk.Entry(self)
        self.expense_limit_entry.grid(row=0, column=1, padx=20, pady=20, sticky="w")

        self.income_goal_label = ttk.Label(self, text=self.get_translation("enter_your_income_goal"))
        self.income_goal_label.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        self.income_goal_entry = ttk.Entry(self)
        self.income_goal_entry.grid(row=0, column=3, padx=20, pady=20, sticky="w")

        self.submit_button = ttk.Button(self, text=self.get_translation("submit"), command=self.submit_goal)
        self.submit_button.grid(row=0, column=4, columnspan=2, pady=20, padx=20)
        
        self.show_chart_button = ttk.Button(self, text=self.get_translation("show_chart"), command=self.show_chart)
        self.show_chart_button.grid(row=1, column=0, columnspan=2, pady=20, padx=20)
        
        self.chart_frame = ttk.Frame(self)
        self.chart_frame.grid(row=2, column=0, columnspan=5, pady=20, padx=20)

        # Fetch and set the previously submitted financial goals
        expense_limit, income_goal = self.viewmodel.get_financial_goal()
        self.expense_limit_entry.insert(0, expense_limit or "")
        self.income_goal_entry.insert(0, income_goal or "")
        
    def show_chart(self):
        expense_limit, income_goal = self.viewmodel.get_financial_goal()
        actual_expense = self.viewmodel.get_actual_expense()
        actual_income = self.viewmodel.get_actual_income()
        
        labels = ['Expense', 'Income']
        goals = [float(expense_limit), float(income_goal)]
        actuals = [actual_expense, actual_income]

        x = range(len(labels))

        fig, ax = plt.subplots()
        ax.bar(x, goals, width=0.4, label='Goal', align='center')
        ax.bar(x, actuals, width=0.4, label='Actual', align='edge')

        ax.set_xlabel('Category')
        ax.set_ylabel('Amount')
        ax.set_title('Financial Goals vs Actuals')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        # Clear the previous chart if it exists
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=ttk.BOTH, expand=True)