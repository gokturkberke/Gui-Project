import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DB_NAME = "finance_manager.db"

class BudgetOverview(tk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.title(self.get_translation("budget_overview"))
        self.geometry("800x600")
        self.init_ui()

    def init_ui(self):
        self.chart_button = tk.Button(self, text=self.get_translation("generate_chart"), command=self.generate_chart)
        self.chart_button.pack(pady=20)

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(expand=True, fill='both')

    def generate_chart(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE type = 'Income'
            GROUP BY category
        """)
        rows = cursor.fetchall()
        conn.close()

        categories = [row[0] for row in rows]
        amounts = [row[1] for row in rows]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
        ax.set_title(self.get_translation("budget_overview"))

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def get_translation(self, key, **kwargs):
        return self.viewmodel.get_translation(key, **kwargs)

    def refresh_ui(self):
        self.title(self.get_translation("budget_overview"))
        self.chart_button.config(text=self.get_translation("generate_chart"))