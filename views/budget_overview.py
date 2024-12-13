import ttkbootstrap as ttk
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry

import matplotlib.pyplot as plt

DB_NAME = "finance_manager.db"

class BudgetOverview(ttk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.title(self.get_translation("budget_overview"))
        self.geometry("1300x850")
        self.init_ui()

    def init_ui(self):
        self.start_date_label = ttk.Label(self, text=self.get_translation("start_date"))
        self.start_date_label.pack(pady=5)
        self.start_date_entry = DateEntry(self)
        self.start_date_entry.pack(pady=5)

        self.end_date_label = ttk.Label(self, text=self.get_translation("end_date"))
        self.end_date_label.pack(pady=5)
        self.end_date_entry = DateEntry(self)
        self.end_date_entry.pack(pady=5)

        self.chart_button = ttk.Button(self, text=self.get_translation("generate_chart"), command=self.generate_charts)
        self.chart_button.pack(pady=20)

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(expand=True, fill='both')

        self.left_frame = ttk.Frame(self.canvas_frame)
        self.left_frame.pack(side='left', expand=True, fill='both')

        self.right_frame = ttk.Frame(self.canvas_frame)
        self.right_frame.pack(side='right', expand=True, fill='both')

    def generate_charts(self):
        self.generate_income_chart()
        self.generate_expense_chart()
        self.generate_remaining_money_chart()

    def generate_income_chart(self):
        start_date = self.start_date_entry.entry.get()
        end_date = self.end_date_entry.entry.get() 
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE type = 'Income' AND date BETWEEN ? AND ?
            GROUP BY category
        """, (start_date, end_date))
        rows = cursor.fetchall()
        conn.close()

        categories = [row[0] for row in rows]
        amounts = [row[1] for row in rows]

        def autopct_format(pct, allvals):
            absolute = int(pct/100.*sum(allvals))
            return f"{pct:.1f}%\n({absolute:d})"

        fig, ax = plt.subplots(figsize=(6, 4))
        wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct=lambda pct: autopct_format(pct, amounts), startangle=140)
        ax.set_title(self.get_translation("income_distribution_by_category"))

        for widget in self.left_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.left_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', expand=True, fill='both')

    def generate_expense_chart(self):
        start_date = self.start_date_entry.entry.get()
        end_date = self.end_date_entry.entry.get() 
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE type = 'Expense' AND date BETWEEN ? AND ?
            GROUP BY category
        """, (start_date, end_date))
        rows = cursor.fetchall()
        conn.close()

        categories = [row[0] for row in rows]
        amounts = [row[1] for row in rows]

        def autopct_format(pct, allvals):
            absolute = int(pct/100.*sum(allvals))
            return f"{pct:.1f}%\n({absolute:d})"

        fig, ax = plt.subplots(figsize=(6, 4))
        wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct=lambda pct: autopct_format(pct, amounts), startangle=140)
        ax.set_title(self.get_translation("expense_distribution_by_category"))

        canvas = FigureCanvasTkAgg(fig, master=self.left_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='bottom', expand=True, fill='both')
    
    def generate_remaining_money_chart(self):
        start_date = self.start_date_entry.entry.get()
        end_date = self.end_date_entry.entry.get()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, SUM(amount)
            FROM transactions
            WHERE date BETWEEN ? AND ?
            GROUP BY type
        """, (start_date, end_date))
        rows = cursor.fetchall()
        conn.close()

        income = sum(row[1] for row in rows if row[0] == 'Income')
        expense = sum(row[1] for row in rows if row[0] == 'Expense')
        remaining = income - expense

        labels = [
            self.get_translation("total_income"),
            self.get_translation("total_expenses"),
            self.get_translation("remaining")
        ]
        amounts = [income, expense, remaining]

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(labels, amounts, color=['green', 'red', 'blue'])
        ax.set_title(self.get_translation("income_vs_expense"))

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', expand=True, fill='both')
            
    def get_translation(self, key, **kwargs):
        return self.viewmodel.get_translation(key, **kwargs)

    def refresh_ui(self):
        self.title(self.get_translation("budget_overview"))
        self.chart_button.config(text=self.get_translation("generate_chart"))