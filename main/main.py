import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from matplotlib import pyplot as plt

# Database setup
DB_NAME = "finance_manager.db"

def setup_database():
    """Set up the SQLite database with a transactions table."""
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

# Language translations
TRANSLATIONS = {
    "en": {
        "title": "Personal Finance Manager",
        "add_income": "Add Income",
        "add_expense": "Add Expense",
        "view_transactions": "View Transactions",
        "budget_overview": "Budget Overview",
        "settings": "Settings",
        "add_transaction": "Add {type}",
        "category": "Category",
        "amount": "Amount",
        "date": "Date (YYYY-MM-DD)",
        "save": "Save",
        "success": "{type} added successfully!",
        "validation_error": "All fields are required!",
        "amount_error": "Amount must be a valid number!",
        "language_changed": "Language set to {language}!",
        "generate_chart": "Generate Chart",
        "language_settings": "Language Settings",
    },
    "tr": {
        "title": "Kişisel Finans Yöneticisi",
        "add_income": "Gelir Ekle",
        "add_expense": "Gider Ekle",
        "view_transactions": "Hareketleri Görüntüle",
        "budget_overview": "Bütçe Genel Görünümü",
        "settings": "Ayarlar",
        "add_transaction": "{type} Ekle",
        "category": "Kategori",
        "amount": "Tutar",
        "date": "Tarih (YYYY-AA-GG)",
        "save": "Kaydet",
        "success": "{type} başarıyla eklendi!",
        "validation_error": "Tüm alanlar doldurulmalıdır!",
        "amount_error": "Tutar geçerli bir sayı olmalıdır!",
        "language_changed": "Dil {language} olarak ayarlandı!",
        "generate_chart": "Grafik Oluştur",
        "language_settings": "Dil Ayarları",
    }
}

# Main Application Class
class PersonalFinanceManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.language = "en"  # Default language
        self.title(self.tr("title"))
        self.geometry("600x400")
        self.init_main_menu()

    def tr(self, key, **kwargs):
        """Translate the given key based on the selected language."""
        translation = TRANSLATIONS.get(self.language, {}).get(key, key)
        return translation.format(**kwargs)

    def init_main_menu(self):
        """Initialize the main menu with buttons."""
        self.clear_frame()
        tk.Label(self, text=self.tr("title"), font=("Arial", 20)).pack(pady=20)

        buttons = [
            (self.tr("add_income"), self.open_add_income),
            (self.tr("add_expense"), self.open_add_expense),
            (self.tr("view_transactions"), self.open_view_transactions),
            (self.tr("budget_overview"), self.open_budget_overview),
            (self.tr("settings"), self.open_settings),
        ]

        for text, command in buttons:
            tk.Button(self, text=text, width=25, command=command).pack(pady=5)

    def clear_frame(self):
        """Clear all widgets in the current frame."""
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

    def update_language(self):
        """Update the language of the main menu."""
        self.init_main_menu()

# Transaction Window
class TransactionWindow(tk.Toplevel):
    def __init__(self, master, transaction_type):
        super().__init__(master)
        self.master = master
        self.transaction_type = transaction_type
        self.title(master.tr("add_transaction", type=transaction_type))
        self.geometry("400x300")

        tk.Label(self, text=master.tr("add_transaction", type=transaction_type), font=("Arial", 16)).pack(pady=10)

        self.category_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar()

        fields = [
            (master.tr("category"), self.category_var),
            (master.tr("amount"), self.amount_var),
            (master.tr("date"), self.date_var),
        ]

        for label, var in fields:
            tk.Label(self, text=label).pack(anchor="w", padx=10)
            tk.Entry(self, textvariable=var).pack(fill="x", padx=10, pady=5)

        tk.Button(self, text=master.tr("save"), command=self.save_transaction).pack(pady=20)

    def save_transaction(self):
        category = self.category_var.get().strip()
        amount = self.amount_var.get().strip()
        date = self.date_var.get().strip()

        if not category or not amount or not date:
            messagebox.showerror(self.master.tr("validation_error"), self.master.tr("validation_error"))
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror(self.master.tr("validation_error"), self.master.tr("amount_error"))
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (type, category, amount, date)
            VALUES (?, ?, ?, ?)
        """, (self.transaction_type, category, amount, date))
        conn.commit()
        conn.close()

        messagebox.showinfo(self.master.tr("success"), self.master.tr("success", type=self.transaction_type))
        self.destroy()

# Transaction Viewer
class TransactionViewer(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title(master.tr("view_transactions"))
        self.geometry("600x400")

        self.tree = ttk.Treeview(self, columns=("Type", "Category", "Amount", "Date"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Category", text=master.tr("category"))
        self.tree.heading("Amount", text=master.tr("amount"))
        self.tree.heading("Date", text=master.tr("date"))
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
        self.master = master
        self.title(master.tr("budget_overview"))
        self.geometry("600x400")

        tk.Button(self, text=master.tr("generate_chart"), command=self.generate_chart).pack(pady=20)

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
        plt.title(self.master.tr("budget_overview"))
        plt.show()

# Settings Window
class SettingsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title(master.tr("settings"))
        self.geometry("400x200")

        tk.Label(self, text=master.tr("language_settings")).pack(pady=20)

        tk.Button(self, text="English", command=lambda: self.set_language("en")).pack(pady=5)
        tk.Button(self, text="Türkçe", command=lambda: self.set_language("tr")).pack(pady=5)

    def set_language(self, lang):
        self.master.language = lang
        self.master.update_language()
        language_name = "English" if lang == "en" else "Türkçe"
        messagebox.showinfo(self.master.tr("language_changed"), self.master.tr("language_changed", language=language_name))

# Run the Application
if __name__ == "__main__":
    setup_database()
    app = PersonalFinanceManager()
    app.mainloop()
