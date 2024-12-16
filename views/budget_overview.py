import ttkbootstrap as ttk
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
import matplotlib.pyplot as plt
from tkinter import messagebox
from datetime import datetime

DB_NAME = "finance_manager.db"

class BudgetOverview(ttk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.title(self.get_translation("budget_overview"))
        self.geometry("1300x1000")
        self.minsize(1300, 1000)
        self.init_ui()

    def init_ui(self):
        self.start_date_label = ttk.Label(self, text=self.get_translation("start_date"))
        self.start_date_label.pack(pady=5)
        self.start_date_entry = DateEntry(self)
        self.start_date_entry.pack(pady=5)
        self.start_date_entry.bind("<<DateEntrySelected>>", self.validate_date_range)

        self.end_date_label = ttk.Label(self, text=self.get_translation("end_date"))
        self.end_date_label.pack(pady=5)
        self.end_date_entry = DateEntry(self)
        self.end_date_entry.pack(pady=5)
        self.end_date_entry.bind("<<DateEntrySelected>>", self.validate_date_range)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=20)
        
        self.chart_button = ttk.Button(self.button_frame, text=self.get_translation("generate_chart"), 
                                    command=self.generate_charts)
        self.chart_button.pack(side='left', padx=5)
        
        self.all_time_button = ttk.Button(self.button_frame, text=self.get_translation("show_all_time"), 
                                        command=self.generate_all_time_charts)
        self.all_time_button.pack(side='left', padx=5)

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(expand=True, fill='both')

        self.left_frame = ttk.Frame(self.canvas_frame)
        self.left_frame.pack(side='left', expand=True, fill='both')

        self.right_frame = ttk.Frame(self.canvas_frame)
        self.right_frame.pack(side='right', expand=True, fill='both')

    def validate_date_range(self, event=None):
        start_date = self.start_date_entry.entry.get()
        end_date = self.end_date_entry.entry.get()
        if start_date and end_date and start_date > end_date:
            messagebox.showwarning(self.get_translation("invalid_date"), self.get_translation("invalid_date_msg"))
            self.end_date_entry.entry.delete(0, 'end')
            self.end_date_entry.entry.insert(0, start_date)
            return False
        return True
    
    def get_date_range(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(date), MAX(date) FROM transactions")
        min_date, max_date = cursor.fetchone()
        conn.close()
        return min_date, max_date

    def generate_all_time_charts(self):
        min_date, max_date = self.get_date_range()
        self.start_date_entry.entry.delete(0, 'end')
        self.start_date_entry.entry.insert(0, min_date)
        self.end_date_entry.entry.delete(0, 'end')
        self.end_date_entry.entry.insert(0, max_date)
        self.generate_charts()
        
    def generate_charts(self):
        if not self.validate_date_range():
            return
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
            return f"{pct:.1f}%\n(${absolute:,.2f})"

        fig, ax = plt.subplots(figsize=(6, 4))
        wedges, texts, autotexts = ax.pie(amounts, labels=categories, 
                                         autopct=lambda pct: autopct_format(pct, amounts), 
                                         startangle=140)
        plt.setp(autotexts, size=8)
        plt.setp(texts, size=8)
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

        # Create the pie chart
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(amounts, labels=categories, startangle=140)  # Removed autopct to hide labels
        ax.set_title(self.get_translation("expense_distribution_by_category"))

        # Embed the chart in the Tkinter window
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
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:,.2f}',
                   ha='center', va='bottom')

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', expand=True, fill='both')

    def get_translation(self, key):
        return self.viewmodel.get_translation(key)
    
    def refresh_ui(self):
        self.title(self.get_translation("budget_overview"))
        self.chart_button.config(text=self.get_translation("generate_chart"))