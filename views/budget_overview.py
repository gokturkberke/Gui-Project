import ttkbootstrap as ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DB_NAME = "finance_manager.db"

class BudgetOverview(ttk.Toplevel):
    def __init__(self, master, viewmodel):
        super().__init__(master)
        self.master = master
        self.viewmodel = viewmodel
        self.title(self.get_translation("budget_overview"))
        self.geometry("800x600")
        self.init_ui()

    def init_ui(self):
        self.chart_button = ttk.Button(self, text=self.get_translation("generate_chart"), command=self.generate_chart)
        self.chart_button.pack(pady=20)

        self.canvas_frame = ttk.Frame(self)
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

        def autopct_format(pct, allvals):
            absolute = int(pct/100.*sum(allvals))
            return f"{pct:.1f}%\n({absolute:d})"

        fig, ax = plt.subplots(figsize=(8, 6))
        wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct=lambda pct: autopct_format(pct, amounts), startangle=140)
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