import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from matplotlib import pyplot as plt
from tkinter import filedialog
import os

# Database setup
DB_NAME = "finance_manager.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Main Application Class
class PersonalFinanceManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Finance Manager")
        self.geometry("600x400")
        self.language = "en"
        self.init_main_menu()

    def init_main_menu(self):
        self.clear_frame()
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

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def open_add_income(self):
        TransactionWindow(self, "Income")

    def open_add_expense(self):
        TransactionWindow(self, "Expense")

    def open_view_transactions(self):
        TransactionViewer(self)

    def open_budget_overview(self):
        BudgetOverview(self)

    def open_settings(self):
        SettingsWindow(self)

# Transaction Window
class TransactionWindow(tk.Toplevel):
    def __init__(self, master, transaction_type):
        super().__init__(master)
        self.transaction_type = transaction_type
        self.title(f"Add {transaction_type}")
        self.geometry("400x300")

        tk.Label(self, text=f"Add {transaction_type}", font=("Arial", 16)).pack(pady=10)

        self.category_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar()

        fields = [
            ("Category", self.category_var),
            ("Amount", self.amount_var),
            ("Date (YYYY-MM-DD)", self.date_var),
        ]

        for label, var in fields:
            tk.Label(self, text=label).pack(anchor="w", padx=10)
            tk.Entry(self, textvariable=var).pack(fill="x", padx=10, pady=5)

        tk.Button(self, text="Save", command=self.save_transaction).pack(pady=20)

    def save_transaction(self):
        category = self.category_var.get().strip()
        amount = self.amount_var.get().strip()
        date = self.date_var.get().strip()

        if not category or not amount or not date:
            messagebox.showerror("Validation Error", "All fields are required!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Validation Error", "Amount must be a valid number!")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (type, category, amount, date)
            VALUES (?, ?, ?, ?)
        """, (self.transaction_type, category, amount, date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"{self.transaction_type} added successfully!")
        self.destroy()

# Transaction Viewer
class TransactionViewer(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("View Transactions")
        self.geometry("600x400")

        self.tree = ttk.Treeview(self, columns=("Type", "Category", "Amount", "Date"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Date", text="Date")
        self.tree.pack(fill="both", expand=True)

        self.load_transactions()

    def load_transactions(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT type, category, amount, date FROM transactions")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

# Budget Overview with Chart
class BudgetOverview(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Budget Overview")
        self.geometry("600x400")

        tk.Button(self, text="Generate Chart", command=self.generate_chart).pack(pady=20)

    def generate_chart(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, SUM(amount) 
            FROM transactions 
            WHERE type = 'Expense' 
            GROUP BY category
        """)
        rows = cursor.fetchall()
        conn.close()

        categories = [row[0] for row in rows]
        amounts = [row[1] for row in rows]

        plt.figure(figsize=(6, 4))
        plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
        plt.title("Expenses by Category")
        plt.show()

# Settings Window
class SettingsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Settings")
        self.geometry("400x200")

        tk.Label(self, text="Language Settings").pack(pady=20)

        tk.Button(self, text="English", command=lambda: self.set_language("en")).pack(pady=5)
        tk.Button(self, text="Turkish", command=lambda: self.set_language("tr")).pack(pady=5)

    def set_language(self, lang):
        self.master.language = lang
        language_name = "English" if lang == "en" else "Turkish"
        messagebox.showinfo("Language Changed", f"Language set to {language_name}!")


# Run the Application
if __name__ == "__main__":
    setup_database()
    app = PersonalFinanceManager()
    app.mainloop()
